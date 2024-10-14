from django.db import models

from sgh_app.models.dias_semana import DiasSemana
from .disciplina_professor import DisciplinaProfessor  # Importando o modelo DisciplinaProfessor
from .ano_semestre import AnoSemestre
from .horario_curso import HorarioCurso  # Importando o modelo HorarioCurso

class HorariosDisciplinas(models.Model):
    # Relacionamento com DisciplinaProfessor (associa uma disciplina a um professor)
    disciplina_professor = models.ForeignKey(DisciplinaProfessor, on_delete=models.CASCADE, related_name='horarios_disciplinas', null=True,)  # Permite valores nulosblank=True  # Permite que o campo fique em branco )
    
    # Relacionamento com HorarioCurso (reutilizando os horários e dias definidos no curso)
    horario_curso = models.ForeignKey(HorarioCurso, on_delete=models.CASCADE, related_name='horarios_disciplinas', default=1)
    
    # Ano e semestre específico para o qual este horário de disciplina está sendo gerado
    ano_semestre = models.ForeignKey(AnoSemestre, on_delete=models.CASCADE, related_name='horarios_disciplinas')

    # Novo campo para armazenar o período
    PERIODO_CHOICES = [
        ('par', 'Par'),
        ('impar', 'Ímpar'),
    ]
    periodo = models.CharField(max_length=5, choices=PERIODO_CHOICES,null=True, blank=True)
    dia_semana = models.ForeignKey(DiasSemana, on_delete=models.CASCADE, default=1)

 
    
    def __str__(self):
            professor_info = self.disciplina_professor if self.disciplina_professor else "Sem professor"
            return f"{professor_info} ({self.horario_curso.hora_inicio} - {self.horario_curso.hora_fim}) - {self.horario_curso.curso} - {self.ano_semestre} - {self.periodo} - {self.dia_semana.nome}"