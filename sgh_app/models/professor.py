# sgh_app/models/professor.py
from django.db import models
from .curso import Curso
from .centro import Centro

class Professor(models.Model):
    nome = models.CharField(max_length=255)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='professores')
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE, related_name='professores')

    def __str__(self):
        return self.nome
