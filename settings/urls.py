from django.urls import path
from . import inventoryCat_view, vendorCat_view

urlpatterns = [

#  Inventory Category
path('inventory/category/', inventoryCat_view.index, name='inventory.category.index'),
path('inventory/category/add/', inventoryCat_view.add, name='inventory.category.add'),
path('inventory/category/list/', inventoryCat_view.list, name='inventory.category.list'),
path('inventory/category/profile/<int:id>/', inventoryCat_view.show, name='inventory.category.show'),
path('inventory/category/save/', inventoryCat_view.save, name = 'inventory.category.save'),
path('inventory/category/update/<int:id>/', inventoryCat_view.update, name = 'inventory.category.update'),
path('inventory/category/delete/<int:id>/', inventoryCat_view.delete, name = 'inventory.category.delete'),


#  Vendor Category 
path('vendor/category/', vendorCat_view.index, name='vendor.category.index'),
path('vendor/category/add/', vendorCat_view.add, name='vendor.category.add'),
path('vendor/category/list/', vendorCat_view.list, name='vendor.category.list'),
path('vendor/category/profile/<int:id>/', vendorCat_view.show, name='vendor.category.show'),
path('vendor/category/save/', vendorCat_view.save, name = 'vendor.category.save'),
path('vendor/category/update/<int:id>/', vendorCat_view.update, name = 'vendor.category.update'),
path('vendor/category/delete/<int:id>/', vendorCat_view.delete, name = 'vendor.category.delete'),


#  Customer Category 
path('vendor/category/', vendorCat_view.index, name='vendor.category.index'),
path('vendor/category/add/', vendorCat_view.add, name='vendor.category.add'),
path('vendor/category/list/', vendorCat_view.list, name='vendor.category.list'),
path('vendor/category/profile/<int:id>/', vendorCat_view.show, name='vendor.category.show'),
path('vendor/category/save/', vendorCat_view.save, name = 'vendor.category.save'),
path('vendor/category/update/<int:id>/', vendorCat_view.update, name = 'vendor.category.update'),
path('vendor/category/delete/<int:id>/', vendorCat_view.delete, name = 'vendor.category.delete'),


]