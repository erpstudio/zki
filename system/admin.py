from django.contrib import admin
from system.models import Employee, Vendor, Customer, Inventory

# Register your models here.
admin.site.register([Employee, Vendor, Customer, Inventory])
