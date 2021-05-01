from django.urls import path
from . import purchase_view

urlpatterns = [

#  Inventory Category
path('purchase/', purchase_view.add, name='purchase.add'),


]