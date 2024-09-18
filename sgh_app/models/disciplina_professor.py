from django.db import models
from .disciplina import Disciplina
from .professor import Professor

class DisciplinaProfessor(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='disciplina_professores')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='disciplina_professores', null=True)


