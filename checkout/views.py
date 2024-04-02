from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
# Create your views here.

def checkout(request):
    shoppingbag = request.session.get('shoppingbag', {})
    if not shoppingbag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51OKevjGkJ5U3ree3hDekfwjx55kbeLxkqd4ZFixTfFSX85MVHCPBSMaJxvG26rq1QUzHyGTD4Pw4A12o5O2hciZm00abo7KSoY',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)