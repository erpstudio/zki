from django.db import models
from datetime import date as dt

from django.utils.translation import ugettext as _
from  system.models import Inventory, Customer

# Sale
class SaleEntry(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, verbose_name=_("Inventory"), on_delete=models.CASCADE)
    unit_price = models.IntegerField(default=0, verbose_name=_("Unit Price"))
    quantity = models.IntegerField(default=0, verbose_name=_("Quantity"))
    total_amount = models.IntegerField(default=0, verbose_name=_("Total Amount"))
    installment_started = models.DateField(default=dt.today, verbose_name=_("Installment Started"))
    installment_interval_days = models.IntegerField(default=0, verbose_name=_("Installment Interval Days"))
    installment_amount = models.IntegerField(default=0, verbose_name=_("Installment Amount"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
