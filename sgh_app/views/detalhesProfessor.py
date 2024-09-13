# sgh_app/views/professor_views.py
from django.shortcuts import render, get_object_or_404
from sgh_app.models.professor import Professor
from sgh_app.models.disciplina_professor import DisciplinaProfessor

def detalhes_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    disciplinas = professor.disciplina_professores.all().select_related('disciplina')
    return render(request, 'detalhes_professor.html', {'professor': professor, 'disciplinas': disciplinas})
