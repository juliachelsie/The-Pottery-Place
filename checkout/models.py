import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product

# Create your models here.

class Order(models.Model):
    order_number = models.CharField(max_length=25, editable=False, null=False)
    name = models.CharField(max_length=55, null=False, blank=False)
    email = models.EmailField(max_length=240, null=False, blank=False)
    phone = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=40, blank=False, null=False)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=85, blank=False, null=False)
    county = models.CharField(max_length=85, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def create_order_number(self):
        """Create a unique ordernumber using uuid """

        return uuid.uuid4().hex.upper()

    def update_total_cost(self):
        """Updates total cost each time a item is added"""
        self.order_total = self.items.aggregate(Sum('item_total'))['item_total__sum']
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total =self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Sets ordernumber if it hasn't been set"""
        if not self.order_number:
            self.order_number = self._create_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number



class OrderItem(models.Model):
    Order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity =models.IntegerField(null=False, blank=False, default=0)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """Sets ordernumber if it hasn't been set"""
        self.item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
