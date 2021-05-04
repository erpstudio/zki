from django.urls import path
from . import saleentry_view, installment_view

urlpatterns = [

#  Installments
path('installment/list', installment_view.list, name='installment.list'),

#  Purchase Entry
path('sale/entry/add', saleentry_view.add, name='sale.entry.add'),
path('sale/entry/list', saleentry_view.list, name='sale.entry.list'),
path('sale/entry/<int:id>/', saleentry_view.show, name='sale.entry.show'),
path('sale/entry/save', saleentry_view.save, name='sale.entry.save'),


]