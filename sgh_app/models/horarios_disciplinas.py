from django.db import models
from .disciplina import Disciplina
from .professor import Professor
from .periodo import Periodo
from .dias_semana import DiasSemana

class HorariosDisciplinas(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='horarios_disciplinas')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='horarios_disciplinas')
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='horarios_disciplinas')
    hora = models.TimeField()
    dia = models.ForeignKey(DiasSemana, on_delete=models.CASCADE, related_name='horarios_disciplinas')
