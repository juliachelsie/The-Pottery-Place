from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_number', 'date', 
                    'delivery_cost', 'order_total',
                    'grand_total', 'originalBag', 
                    'stripe_pid')
    
    fields = ('order_number', 'date', 'name',
                'email', 'phone', 'country',
                'post_code', 'city', 'address',
                'county', 'delivery_cost',
                'order_total', 'grand_total',
                 'originalBag', 'stripe_pid')
    
    list_display = ('order_number', 'date', 'name',
                    'order_total','delivery_cost', 'grand_total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)