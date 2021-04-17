from django.db import models

# Create your models here.

class VendorCategory(models.Model):
    name = models.CharField(max_length=30)

class EmployeeCategory(models.Model):
    name = models.CharField(max_length=30)

class InventoryCategory(models.Model):
    name = models.CharField(max_length=30)

class InventoryUnits(models.Model):
    name = models.CharField(max_length=30)

class AreaZone(models.Model):
    name = models.CharField(max_length=30)