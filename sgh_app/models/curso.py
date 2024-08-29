from django.db import models
from sgh_app.models.centro import Centro

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    quantidade_periodos = models.PositiveIntegerField()
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
