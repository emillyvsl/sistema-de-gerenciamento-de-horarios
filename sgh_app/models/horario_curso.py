from django.db import models
from .curso import Curso

class HorarioCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='horarios')
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fim}"


