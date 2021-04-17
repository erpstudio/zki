from django.contrib import admin
from settings.models import EmployeeCategory, VendorCategory, InventoryCategory, InventoryUnits, AreaZone

# Register your models here.
admin.site.register([EmployeeCategory, VendorCategory, InventoryCategory, InventoryUnits, AreaZone])