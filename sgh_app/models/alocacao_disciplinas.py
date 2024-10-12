from sgh_app import models
from sgh_app.models.disciplina_professor import DisciplinaProfessor
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from django.db import models


class AlocacaoDisciplinas(models.Model):
    horarios_disciplinas = models.ForeignKey(HorariosDisciplinas, on_delete=models.CASCADE, related_name='alocacoes')
    disciplina_professor = models.ForeignKey(DisciplinaProfessor, on_delete=models.CASCADE, related_name='alocacoes')

    def __str__(self):
        return f"{self.disciplina_professor.disciplina.nome} - {self.disciplina_professor.professor.nome} ({self.horarios_disciplinas})"