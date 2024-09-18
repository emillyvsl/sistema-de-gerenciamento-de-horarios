from django.db import models
from .semestre import Semestre

class AnoSemestre(models.Model):
    ano = models.IntegerField()
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='ano_semestres')
    
    class Meta:
        unique_together = ('ano', 'semestre')  # Garante que não haja duplicidade de ano e semestre

    def __str__(self):
        return f'{self.ano} - {self.semestre}'
