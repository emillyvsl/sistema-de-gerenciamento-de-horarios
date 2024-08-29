from django.db import models
from django.contrib.auth.models import User
from .curso import Curso
from sgh_app.models.curso import Curso

class Coordenacao(models.Model):
    nome = models.CharField(max_length=255)
    curso = models.OneToOneField(Curso, on_delete=models.CASCADE, related_name='coordenacao')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coordenacao')

    def __str__(self):
        return self.nome