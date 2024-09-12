from django.db import models
from .curso import Curso
from .tipo_periodo import TipoPeriodo

class Periodo(models.Model):
    tipo_periodo = models.OneToOneField(TipoPeriodo, on_delete=models.CASCADE, related_name='periodos')

    def __str__(self):
        return self.tipo_periodo.nome