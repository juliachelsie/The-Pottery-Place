from django import template

register = template.Library()

@register.filter(name='calculate_sub_total')
def calculate_sub_total(price, quantity):
    
    return price * quantity