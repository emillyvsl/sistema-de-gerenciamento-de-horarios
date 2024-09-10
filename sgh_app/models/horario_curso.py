from django.db import models
from .curso import Curso

class HorarioCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='horarios')
    hora = models.TimeField()
