from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone = models.CharField(max_length=30, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', blank=True, null=True)
    default_post_code = models.CharField(max_length=20, null=True, blank=True)
    default_city = models.CharField(max_length=50, null=True, blank=True)
    default_address = models.CharField(max_length=85, blank=True, null=True)
    default_county = models.CharField(max_length=85, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
