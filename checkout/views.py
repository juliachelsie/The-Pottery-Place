from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import OrderForm
from django.conf import settings
from products.models import Product
from shoppingbag.contexts import shoppingbag_contents
from .models import Order, OrderItem

import stripe
import json
# Create your views here.

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'shoppingbag': json.dumps(request.session.get('shoppingbag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Your payment cannot be processed right now, Please try againg later.')
        return HttpResponse(content=e, status=400)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        shoppingbag = request.session.get('shoppingbag', {})

        form_data = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'country': request.POST['country'],
            'post_code': request.POST['post_code'],
            'city': request.POST['city'],
            'address': request.POST['address'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in shoppingbag.items():
                try:
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

                except Product.DoesNotExist:
                    messages.error(request, (
                        "We can't find one or more products in your shopping bag in our data base."
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_shoppingbag'))
            
            request.session['save_info'] = 'save_info' in request.POST
            return redirect(reverse('success_checkout', args=[order.order_number]))  
        else:
            messages.error(request, 'A error occured, Please check your information')

    else:
        shoppingbag = request.session.get('shoppingbag', {})
        if not shoppingbag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        shoppingbag_now = shoppingbag_contents(request)
        total = shoppingbag_now['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing, is it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def success_checkout(request, order_number):
    """Handles successful checkouts"""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successful! \
        Your order number is {order_number}. A confirmation email \
            will be sent to {order.email}')

    if 'shoppingbag' in request.session:
        del request.session['shoppingbag']
    
    template = 'checkout/success_checkout.html'
    context = {
        'order': order,
    }
    
    return render(request, template, context)