from django.http import HttpResponse

from .models import Order, OrderItem
from products.models import Product

import json
import time

class StripeWH_Handler:
    """Handle stripe webhooks"""
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle unknown webhook event """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ Handle payment_intent.succeded webhook from stripe """
        intent = event.data.object
        pid = intent.id
        shoppingbag = intent.metadata.shoppingbag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
        intent.latest_charge
    )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value =="":
                shipping_details.address[field] = None

        order_exists = False 
        attempt = 1
        while attempt <= 5:

            try:
                order = Order.objects.get(
                    name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.post_code,
                    city__iexact=shipping_details.address.city,
                    address__iexact=shipping_details.address.address,
                    county__iexact=shipping_details.adress.county,
                    grand_total=grand_total,
                    originalBag=shoppingbag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
                
            except Order.DoesNotExists:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                name=details.name,
                email=billing_details.email,
                phone=shipping_details.phone,
                country=shipping_details.address.country,
                postcode=shipping_details.address.post_code,
                city=shipping_details.address.city,
                address=shipping_details.address,
                county=shipping_details.address.county,
                originalBag=shoppingbag,
                stripe_pid=pid,
                )
                for item_id, item_data in json.loads(shoppingbag).items():
                    product = Product.objects.get(id=item_id)
                if isinstance(item_data, int):
                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_item.save()
                else:
                    for quantity in item_data.items():
                        order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook recieved: {event['type']} | Error: {e}',
                status=500)

        return HttpResponse(
            content=f'Webhook recieved: {event['type']} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle payment_intent.payment_failed webhook from stripe """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
