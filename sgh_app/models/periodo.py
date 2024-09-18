from django.db import models
from .tipo_periodo import TipoPeriodo

class Periodo(models.Model):
    tipo_periodo = models.ForeignKey(TipoPeriodo, on_delete=models.CASCADE, related_name='periodos')
    numero = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.numero} - {self.tipo_periodo}'

    def get_nome_periodo(self):
        return f'{self.numero} - {self.tipo_periodo}'
