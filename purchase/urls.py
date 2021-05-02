from django.urls import path
from . import purchase_view

urlpatterns = [

#  Purchase Entry
path('purchase/entry/add', purchase_view.add, name='purchase.entry.add'),
path('purchase/entry/list', purchase_view.list, name='purchase.entry.list'),
path('purchase/entry/<int:id>/', purchase_view.show, name='purchase.entry.show'),
path('purchase/entry/save', purchase_view.save, name='purchase.entry.save'),


]