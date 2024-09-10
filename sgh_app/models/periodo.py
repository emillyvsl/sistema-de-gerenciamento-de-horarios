from django.db import models
from .curso import Curso
from .tipo_periodo import TipoPeriodo

class Periodo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='periodos')
    tipo_periodo = models.OneToOneField(TipoPeriodo, on_delete=models.CASCADE, related_name='periodos')
