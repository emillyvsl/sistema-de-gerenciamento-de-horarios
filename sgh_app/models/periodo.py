from django.db import models
from .semestre import Semestre

class Periodo(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='periodos')
    numero = models.IntegerField('Periodo', default=1)

    def __str__(self):
        return f'{self.numero} Período do {self.semestre}'

    def get_nome_periodo(self):
        return f'{self.numero} Período do {self.semestre}'
