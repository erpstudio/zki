from django.urls import path
from . import inventory_view, dashboard_view

urlpatterns = [

path('', dashboard_view.index, name = 'dashboard'),
path('inventory/', inventory_view.index, name='inventory.index'),
path('inventory/<int:pk>/', inventory_view.show, name='show'),
path('inventory/add/', inventory_view.add, name='inventory.add'),
path('inventory/save/', inventory_view.save, name = 'inventory.save'),
path('inventory/update/', inventory_view.update, name = 'inventory.update'),
path('inventory/delete/', inventory_view.delete, name = 'inventory.delete'),
]