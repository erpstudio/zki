from django.urls import path
from . import inventoryCat_view, inventoryUnit_view, vendorCat_view, areaZone_view

urlpatterns = [

#  Area Zone
path('areazone/', areaZone_view.index, name='areazone.index'),
path('areazone/add/', areaZone_view.add, name='areazone.add'),
path('areazone/list/', areaZone_view.list, name='areazone.list'),
path('areazone/profile/<int:id>/', areaZone_view.show, name='areazone.show'),
path('areazone/save/', areaZone_view.save, name = 'areazone.save'),
path('areazone/update/<int:id>/', areaZone_view.update, name = 'areazone.update'),
path('areazone/delete/<int:id>/', areaZone_view.delete, name = 'areazone.delete'),


#  Inventory Category
path('inventory/category/', inventoryCat_view.index, name='inventory.category.index'),
path('inventory/category/add/', inventoryCat_view.add, name='inventory.category.add'),
path('inventory/category/list/', inventoryCat_view.list, name='inventory.category.list'),
path('inventory/category/profile/<int:id>/', inventoryCat_view.show, name='inventory.category.show'),
path('inventory/category/save/', inventoryCat_view.save, name = 'inventory.category.save'),
path('inventory/category/update/<int:id>/', inventoryCat_view.update, name = 'inventory.category.update'),
path('inventory/category/delete/<int:id>/', inventoryCat_view.delete, name = 'inventory.category.delete'),

#  Inventory Units
path('inventory/unit/', inventoryUnit_view.index, name='inventory.unit.index'),
path('inventory/unit/add/', inventoryUnit_view.add, name='inventory.unit.add'),
path('inventory/unit/list/', inventoryUnit_view.list, name='inventory.unit.list'),
path('inventory/unit/profile/<int:id>/', inventoryUnit_view.show, name='inventory.unit.show'),
path('inventory/unit/save/', inventoryUnit_view.save, name = 'inventory.unit.save'),
path('inventory/unit/update/<int:id>/', inventoryUnit_view.update, name = 'inventory.unit.update'),
path('inventory/unit/delete/<int:id>/', inventoryUnit_view.delete, name = 'inventory.unit.delete'),


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