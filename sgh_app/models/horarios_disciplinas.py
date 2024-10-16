from django.db import models
from sgh_app.models.dias_semana import DiasSemana
from .disciplina_professor import DisciplinaProfessor
from .ano_semestre import AnoSemestre
from .horario_curso import HorarioCurso
from .curso import Curso  # Importando o modelo Curso

class HorariosDisciplinas(models.Model):
    # Relacionamento com DisciplinaProfessor
    disciplina_professor = models.ForeignKey(DisciplinaProfessor, on_delete=models.CASCADE, related_name='horarios_disciplinas', null=True)

    # Relacionamento com HorarioCurso
    horario_curso = models.ForeignKey(HorarioCurso, on_delete=models.CASCADE, related_name='horarios_disciplinas')

    # Ano e semestre específico
    ano_semestre = models.ForeignKey(AnoSemestre, on_delete=models.CASCADE, related_name='horarios_disciplinas')

    # Período (Par ou Ímpar)
    PERIODO_CHOICES = [
        ('par', 'Par'),
        ('impar', 'Ímpar'),
    ]
    periodo = models.CharField(max_length=5, choices=PERIODO_CHOICES, null=True, blank=True)

    # Relacionamento com Dias da Semana
    dia_semana = models.ForeignKey(DiasSemana, on_delete=models.CASCADE)

    # Adicionando o relacionamento com o modelo Curso
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='horarios_disciplinas')

    class Meta:
        unique_together = (('horario_curso', 'dia_semana', 'periodo', 'ano_semestre'),)

    def __str__(self):
        professor_info = self.disciplina_professor if self.disciplina_professor else "Sem professor"
        return f"{professor_info} ({self.horario_curso.hora_inicio} - {self.horario_curso.hora_fim}) - {self.horario_curso.curso} - {self.ano_semestre} - {self.periodo} - {self.dia_semana.nome} - {self.curso.nome}"
