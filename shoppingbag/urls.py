from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_shoppingbag, name='view_shoppingbag'),
    path('add/<item_id>/', views.add_bag, name='add_bag'),
    path('modify/<item_id>/', views.modify_bag, name='modify_bag'),
    path('remove/<item_id>/', views.remove_bag, name='remove_bag'),
]
