from django.db import models

class data_prueba_tecnica(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=20, null=True)
    company_id = models.CharField(max_length=40, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=20)
    created_at = models.CharField(max_length=255) 
    paid_at = models.CharField(max_length=10, null=True)  

    def __str__(self):
        return self.name
