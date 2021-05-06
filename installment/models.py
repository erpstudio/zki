from django.db import models
import datetime as dt
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
    quantity = models.IntegerField(default=1, verbose_name=_("Quantity"))
    total_amount = models.IntegerField(default=0, verbose_name=_("Total Amount"))
    first_installment_date = models.DateField(default=dt.date.today, verbose_name=_("Installment Started From"))
    installment_cycle = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_("Installment Cycle Days"))
    installment_amount = models.IntegerField(default=0, validators=[MinValueValidator(1)], verbose_name=_("Installment Amount"))
    no_of_installments = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_("Total Installments"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        customer = Customer.objects.get(id=self.customer.id)
        customer.balance = customer.balance+self.total_amount
        customer.save()
        inventory = Inventory.objects.get(id=self.inventory.id)
        inventory.in_stock = inventory.in_stock-self.quantity
        inventory.save()

        super().save(*args, **kwargs)

        scheduled_date = self.first_installment_date
        for number in range(self.no_of_installments):
            
            sch_installment_save = InstallmentSchedule.objects.create(
                sale_entry = self,
                installment_amount = self.installment_amount,
                scheduled_date = scheduled_date
            )
            sch_installment_save.save()
            
            scheduled_date = scheduled_date + dt.timedelta(self.installment_cycle)

            
        sc_installaments = InstallmentSchedule.objects.all()
        print(sc_installaments)


class InstallmentSchedule(models.Model):
    sale_entry = models.ForeignKey(SaleEntry, verbose_name=_("Sale Entry"), on_delete=models.CASCADE)
    installment_amount = models.IntegerField(default=0, verbose_name=_("Installment Amount"))
    scheduled_date = models.DateField(default=dt.date.today, verbose_name=_("Paying Date"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ScheduledInstallmentPayment(models.Model):
    scheduled_installment = models.ForeignKey(InstallmentSchedule, verbose_name=_("Scheduled Installment"), on_delete=models.CASCADE)
    paid_amount = models.IntegerField(default=0, verbose_name=_("Paid Amount"))
    date = models.DateField(default=dt.date.today, verbose_name=_("Paid Date"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)