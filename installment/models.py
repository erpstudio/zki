from django.db import models
from datetime import date as dt
from django.core.validators import MinValueValidator

from django.utils.translation import ugettext as _
from  system.models import Inventory, Customer
from  settings.models import AreaZone

# Sale
class SaleEntry(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, verbose_name=_("Inventory"), on_delete=models.CASCADE)
    areazone = models.ForeignKey(AreaZone, verbose_name=_("Area Zone"), on_delete=models.CASCADE)
    unit_price = models.IntegerField(default=0, verbose_name=_("Unit Price"))
    quantity = models.IntegerField(default=0, verbose_name=_("Quantity"))
    total_amount = models.IntegerField(default=0, verbose_name=_("Total Amount"))
    first_installment_date = models.DateField(default=dt.today, verbose_name=_("Installment Started From"))
    recent_installment_date = models.DateField(verbose_name=_("Recent Installment Date"))
    installment_interval_days = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_("Installment Interval Days"))
    installment_amount = models.IntegerField(default=0, verbose_name=_("Installment Amount"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        customer = Customer.objects.get(id=self.customer.id)
        customer.balance = customer.balance+self.total_amount
        customer.save()
        inventory = Inventory.objects.get(id=self.inventory.id)
        inventory.in_stock = inventory.in_stock-self.quantity
        inventory.save()

        self.recent_installment_date = self.first_installment_date
        super().save(*args, **kwargs)