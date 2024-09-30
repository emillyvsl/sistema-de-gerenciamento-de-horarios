from django.db import models
from .disciplina_professor import DisciplinaProfessor  # Importando o modelo DisciplinaProfessor
from .ano_semestre import AnoSemestre
from .horario_curso import HorarioCurso  # Importando o modelo HorarioCurso

class HorariosDisciplinas(models.Model):
    # Relacionamento com DisciplinaProfessor (associa uma disciplina a um professor)
    disciplina_professor = models.ForeignKey(DisciplinaProfessor, on_delete=models.CASCADE, related_name='horarios_disciplinas')
    
    # Relacionamento com HorarioCurso (reutilizando os horários e dias definidos no curso)
    horario_curso = models.ForeignKey(HorarioCurso, on_delete=models.CASCADE, related_name='horarios_disciplinas', default=1)
    
    # Ano e semestre específico para o qual este horário de disciplina está sendo gerado
    ano_semestre = models.ForeignKey(AnoSemestre, on_delete=models.CASCADE, related_name='horarios_disciplinas')

    class Meta:
        unique_together = ('disciplina_professor', 'horario_curso', 'ano_semestre')

    def __str__(self):
        return f"{self.disciplina_professor} ({self.horario_curso.hora_inicio} - {self.horario_curso.hora_fim}) - {self.horario_curso.curso} - {self.ano_semestre}"

    