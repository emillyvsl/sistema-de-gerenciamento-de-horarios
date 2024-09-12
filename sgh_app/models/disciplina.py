from django.db import models

from sgh_app.models.periodo import Periodo
from .curso import Curso

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='disciplinas')
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='disciplinas')

    def __str__(self):
        return self.nome