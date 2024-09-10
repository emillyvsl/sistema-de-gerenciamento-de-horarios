from django.db import models
from .professor import Professor
from .dias_semana import DiasSemana
from .horario_curso import HorarioCurso

class Preferencias(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='preferencias')
    dias_preferidos = models.ManyToManyField(DiasSemana, related_name='preferidos')
    horas_preferidas = models.ManyToManyField(HorarioCurso, related_name='preferidas')
