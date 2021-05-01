from django.db import models
from settings.models import EmployeeCategory, VendorCategory, AreaZone, InventoryCategory, InventoryUnits
from django.utils.translation import ugettext as _
from django.utils import timezone
# Inventory
class Inventory(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Name"))
    unit =  models.ForeignKey(InventoryUnits, verbose_name=_("Unit"), on_delete=models.CASCADE)
    category = models.ForeignKey(InventoryCategory, verbose_name=_("Category"), on_delete=models.CASCADE)
    purchase_price = models.IntegerField(default=0, verbose_name=_("Purchase Price"))
    sale_price = models.IntegerField(default=0, verbose_name=_("Sale Price"))
    in_stock = models.IntegerField(default=0, verbose_name=_("In Stock"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

# Employes
class Employee(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Name"))
    father_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Father Name"))
    cnic = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("CNIC"))
    mobile = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Mobile"))
    address = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Address"))
    salary = models.IntegerField(default=0, verbose_name=_("Salary"))
    category = models.ForeignKey(EmployeeCategory, on_delete=models.CASCADE, verbose_name=_("Category"))

    def __str__(self):
        return "%s" % (self.name)

## Vendors
class Vendor(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Name"))
    father_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Father Name"))
    cnic = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("CNIC"))
    mobile = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Mobile"))
    address = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Address"))
    category = models.ForeignKey(VendorCategory, on_delete=models.CASCADE, verbose_name=_("Category"))
    balance = models.IntegerField(default=0, verbose_name=_("Balance"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name)



## Customers
class CustomerGuarantor(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Name"))
    father_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Father Name"))
    cnic = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Address"))
    mobile = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Address"))
    address = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Address"))
    occupation = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Occupation"))
    balance = models.IntegerField(default=0, verbose_name=_("Balance"))
    area_zone = models.ForeignKey(AreaZone, on_delete=models.CASCADE, verbose_name=_("Area Zone"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

## Customers
class Customer(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Name"))
    father_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Father Name"))
    cnic = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("CNIC"))
    mobile = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Mobile"))
    address = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Address"))
    occupation = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Occupation"))
    balance = models.IntegerField(default=0, verbose_name=_("Balance"))
    area_zone = models.ForeignKey(AreaZone, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Area Zone"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name)
