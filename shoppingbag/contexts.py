from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def shoppingbag_contents(request):

    shoppingbag_items = []
    total = 0
    product_number = 0
    shoppingbag = request.session.get('shoppingbag', {})

    for item_id, quantity in shoppingbag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_number += quantity
        shoppingbag_items.append({
            'item_id' : item_id,
            'quantity': quantity,
            'product': product,
        })


    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total *  Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0 
    
    grand_total = delivery + total

    context = {
        'shoppingbag_items' : shoppingbag_items,
        'total' : total,
        'product_number' : product_number,
        'delivery' : delivery,
        'free_delivery_delta' : free_delivery_delta,
        'free_delivery_threshold' : settings.FREE_DELIVERY_THRESHOLD,
        'grand_total' : grand_total,

        
    }

    return context