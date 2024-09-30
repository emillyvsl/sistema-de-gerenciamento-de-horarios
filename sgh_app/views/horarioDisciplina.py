from django.shortcuts import render

from sgh_app.models.horarios_disciplinas import HorariosDisciplinas


def horarioDisciplina(request):
    horarios_disciplinas = HorariosDisciplinas.objects.select_related(
        'disciplina_professor__disciplina', 
        'disciplina_professor__professor', 
        'horario_curso__curso',
        'ano_semestre'
    ).prefetch_related('horario_curso__dias_semana')  # Carregar os dias da semana também

    context = {
        'horarios_disciplinas': horarios_disciplinas,
    }
    return render(request, 'horarios/horarios_disciplinas.html', context)
