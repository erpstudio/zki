from django.urls import path
from . import inventory

urlpatterns = [
path('', inventory.index, name = 'index'),
]