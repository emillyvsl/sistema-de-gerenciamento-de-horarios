from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.semestre import Semestre

@login_required
def horarioDisciplina(request):
    coordenacao = request.user.coordenacao

    if not coordenacao:
        messages.error(request, "Acesso negado: você não possui coordenação associada.")
        return redirect('home')

    curso = coordenacao.curso

    # Buscando todos os anos e semestres disponíveis para o curso
    anos_semestres = HorarioCurso.objects.filter(curso=curso).distinct()

    # Buscando os horários relacionados, com o uso de select_related para melhorar a performance
    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso
    ).select_related(
        'disciplina_professor__disciplina', 
        'disciplina_professor__professor',
        'ano_semestre'
    )

    context = {
        'anos_semestres': anos_semestres,
        'horarios': horarios,
    }

    return render(request, 'horarios/horarios_disciplinas.html', context)
