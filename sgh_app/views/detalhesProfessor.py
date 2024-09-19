# sgh_app/views/professor_views.py
from django.shortcuts import render, get_object_or_404
from sgh_app.models.professor import Professor
from sgh_app.models.disciplina_professor import DisciplinaProfessor
from sgh_app.models.dias_semana import DiasSemana  # Ajuste o nome do import conforme seu arquivo
from sgh_app.models.horario_curso import HorarioCurso  # Ajuste o nome do import conforme seu arquivo

def detalhes_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    disciplinas = professor.disciplina_professores.all().select_related('disciplina')
    dias_semana = DiasSemana.objects.all()
    horarios_curso = HorarioCurso.objects.filter(curso=professor.curso)
    preferencias = professor.preferencias.all()  

    return render(request, 'detalhes_professor.html', {
        'professor': professor,
        'disciplinas': disciplinas,
        'dias_semana': dias_semana,
        'horarios_curso': horarios_curso,
        'preferencias': preferencias,  
    })
