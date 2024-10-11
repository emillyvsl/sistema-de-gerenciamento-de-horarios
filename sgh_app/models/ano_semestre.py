from django.db import models
from .semestre import Semestre
from .curso import Curso  # Importe o modelo de Curso

class AnoSemestre(models.Model):
    ano = models.IntegerField()
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='ano_semestres')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default=1)  # Ajuste para o ID correto do curso

    class Meta:
        unique_together = ('ano', 'semestre', 'curso')  # Unicidade por ano, semestre e curso

    def __str__(self):
        return f'{self.ano} - {self.semestre} ({self.curso})'
