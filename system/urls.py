from django.urls import path
from . import dashboard_view, inventory_view, vendor_view, employee_view

urlpatterns = [

path('', dashboard_view.index, name = 'dashboard'),

#  Inventory 
path('inventory/', inventory_view.index, name='inventory.index'),
path('inventory/add/', inventory_view.add, name='inventory.add'),
path('inventory/list/', inventory_view.list, name='inventory.list'),
path('inventory/profile/<int:id>/', inventory_view.show, name='inventory.show'),
path('inventory/save/', inventory_view.save, name = 'inventory.save'),
path('inventory/update/<int:id>/', inventory_view.update, name = 'inventory.update'),
path('inventory/delete/<int:id>/', inventory_view.delete, name = 'inventory.delete'),

#  Vendor 
path('vendor/', vendor_view.index, name='vendor.index'),
path('vendor/add/', vendor_view.add, name='vendor.add'),
path('vendor/list/', vendor_view.list, name='vendor.list'),
path('vendor/profile/<int:id>/', vendor_view.show, name='vendor.show'),
path('vendor/save/', vendor_view.save, name = 'vendor.save'),
path('vendor/update/<int:id>/', vendor_view.update, name = 'vendor.update'),
path('vendor/delete/<int:id>/', vendor_view.delete, name = 'vendor.delete'),

#  Emploee 
path('employee/', employee_view.index, name='employee.index'),
path('employee/add/', employee_view.add, name='employee.add'),
path('employee/list/', employee_view.list, name='employee.list'),
path('employee/profile/<int:id>/', employee_view.show, name='employee.show'),
path('employee/save/', employee_view.save, name = 'employee.save'),
path('employee/update/<int:id>/', employee_view.update, name = 'employee.update'),
path('employee/delete/<int:id>/', employee_view.delete, name = 'employee.delete'),


]