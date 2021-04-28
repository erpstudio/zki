from django.db import models

# Create your models here.

class VendorCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

class EmployeeCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

class InventoryCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30, blank=True, null=True)
    
    def __str__(self):
        return "%s" % (self.name)

class InventoryUnits(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

class AreaZone(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)