from django.db import models

class Company(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    name = models.CharField(max_length=130, null=True)

class Charge(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=30)
    created_at = models.DateField()
    updated_at = models.DateField(null=True, blank=True)
