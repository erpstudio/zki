from django.db import models
from settings.models import EmployeeCategory, VendorCategory, AreaZone, InventoryCategory, InventoryUnits


# Inventory
class Inventory(models.Model):
    name = models.CharField(max_length=30)
    unit =  models.ForeignKey(InventoryUnits, on_delete=models.CASCADE)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE)
    purchase_price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    total_qty = models.IntegerField(default=0)

# Employes
class Employee(models.Model):
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, null=True)
    cnic = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    salary = models.IntegerField(default=0)
    category = models.ForeignKey(EmployeeCategory, on_delete=models.CASCADE)

## Vendors
class Vendor(models.Model):
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, null=True)
    cnic = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    salary = models.IntegerField(default=0)
    category = models.ForeignKey(VendorCategory, on_delete=models.CASCADE)


## Customers
class Customer(models.Model):
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, null=True)
    cnic = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    balance = models.IntegerField(default=0)
    area_zone = models.ForeignKey(AreaZone, on_delete=models.CASCADE)
