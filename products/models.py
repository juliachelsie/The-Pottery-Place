from django.db import models

# Create your models here.
 
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', related_name='search_box', null=True, blank= True, on_delete=models.SET_NULL)
    description = models.TextField()
    sku = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    product_id = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=200)
    friendly_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name