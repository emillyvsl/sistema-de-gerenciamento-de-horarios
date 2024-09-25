from django.db import models
from .curso import Curso
from .dias_semana import DiasSemana  # Certifique-se de importar o modelo correto

class HorarioCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='horarios')
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    dias_semana = models.ManyToManyField(DiasSemana, related_name='horarios')

    def __str__(self):
        dias = ', '.join([dia.nome for dia in self.dias_semana.all()])
        return f"{self.hora_inicio} a {self.hora_fim} ({dias})"
