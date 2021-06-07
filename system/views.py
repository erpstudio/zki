from django.views.generic import CreateView
from models import Inventory


class InventoryCreateView(CreateView):
    model = Inventory
    fields = ('name', 'unit', 'category', 'purchase_price')
