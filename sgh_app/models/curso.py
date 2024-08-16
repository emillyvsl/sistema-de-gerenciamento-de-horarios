from django.db import models
from sgh_app.models.centro import Centro

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    centro_id = models.ForeignKey(Centro, on_delete=models.CASCADE)
