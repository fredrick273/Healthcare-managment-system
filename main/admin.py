from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Patient)
admin.site.register(models.Dept)
admin.site.register(models.Employee)
admin.site.register(models.Appointment)
admin.site.register(models.PharmacyBill)
admin.site.register(models.PharmacyItem)
admin.site.register(models.PharmacyItemQuantity)
admin.site.register(models.Prescription)
admin.site.register(models.Test)
admin.site.register(models.LabTestResult)
