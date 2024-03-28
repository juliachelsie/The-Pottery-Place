from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_shoppingbag(request):
    """ A view that renders the shoppingbag content page """
    
    return render(request, 'shoppingbag/shoppingbag.html')

def add_bag(request, item_id):
    """ A view to add a quantity of a specified product to shopping bag """
    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    shoppingbag = request.session.get('shoppingbag', {})

    if item_id in list(shoppingbag.keys()):
        shoppingbag[item_id] += quantity
    else:
        shoppingbag[item_id] = quantity
        messages.success(request, f'Successfully added {product.name} to your bag.')

    request.session['shoppingbag'] = shoppingbag
    return redirect(redirect_url)


def modify_bag(request, item_id):
    """ Modify the quantity of a product in the shoppingbag """
    quantity = int(request.POST.get('quantity'))
    shoppingbag = request.session.get('shoppingbag', {})
    
    if quantity:
        if quantity > 0:
            shoppingbag[item_id]=quality
    else:
        del bag[item_id]
        if not shoppingbag[item_id]:
            shoppingbag.pop(item_id)
        

    request.session['shoppingbag'] = shoppingbag
    return redirect(reverse('view_shoppingbag'))

def remove_bag(request, item_id):
    """ Remove product from the shoppingbag """
    quantity = int(request.POST.get('quantity'))
    shoppingbag = request.session.get('shoppingbag', {})
    
    try:
        if quantity > 0:
            shoppingbag[item_id] = quantity
        else:
            shoppingbag.pop[item_id]

        request.session['shoppingbag'] = shoppingbag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)
