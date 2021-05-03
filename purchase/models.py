from django.db import models
from django.utils.translation import ugettext as _
from  system.models import Vendor, Inventory
from datetime import date as dt

# Purchase
class PurchaseEntry(models.Model):
    vendor =  models.ForeignKey(Vendor, verbose_name=_("Vendor"), on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, verbose_name=_("Inventory"), on_delete=models.CASCADE)
    unit_price = models.IntegerField(default=0, verbose_name=_("Unit Price"))
    quantity = models.IntegerField(default=0, verbose_name=_("Quantity"))
    total_amount = models.IntegerField(default=0, verbose_name=_("Total Amount"))
    # date = models.DateField(default=dt.today, verbose_name=_("Date"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)