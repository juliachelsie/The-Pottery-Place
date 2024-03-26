from django.shortcuts import render, redirect

# Create your views here.

def view_shoppingbag(request):
    """ A view that renders the shoppingbag content page """
    
    return render(request, 'shoppingbag/shoppingbag.html')

def add_bag(request, item_id):
    """ A view to add a quantity of a specified product to shopping bag """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    shoppingbag = request.session.get('shoppingbag', {})

    if item_id in list(shoppingbag.keys()):
        shoppingbag[item_id] += quantity
    else:
        shoppingbag[item_id] = quantity

    request.session['shoppingbag'] = shoppingbag
    return redirect(redirect_url)
