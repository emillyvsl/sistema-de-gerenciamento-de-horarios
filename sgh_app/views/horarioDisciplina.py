from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.semestre import Semestre
from sgh_app.models.ano_semestre import AnoSemestre

@login_required
def horarioDisciplina(request):
    coordenacao = request.user.coordenacao

    if not coordenacao:
        messages.error(request, "Acesso negado: você não possui coordenação associada.")
        return redirect('home')

    curso = coordenacao.curso

    # Buscar os semestres disponíveis
    semestres = Semestre.objects.all()

    # Filtrando por ano e semestre se houver na requisição
    ano = request.GET.get('ano')
    semestre_id = request.GET.get('semestre')

    # Buscar horários
    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso
    ).select_related(
        'disciplina_professor__disciplina',
        'disciplina_professor__professor',
        'ano_semestre',
        'horario_curso'
    ).prefetch_related('horario_curso__dias_semana')

    if ano:
        horarios = horarios.filter(ano_semestre__ano=ano)
    if semestre_id:
        horarios = horarios.filter(ano_semestre__semestre_id=semestre_id)

    # Caso não haja filtro, pegar o quadro mais recente
    if not ano and not semestre_id:
        ultimo_ano_semestre = AnoSemestre.objects.latest('ano', 'semestre')
        horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
        pesquisa_realizada = False  # Não foi realizada pesquisa
    else:
        pesquisa_realizada = True

    context = {
        'horarios': horarios,
        'semestres': semestres,
        'pesquisa_realizada': pesquisa_realizada,
    }

    return render(request, 'horarios/horarios_disciplinas.html', context)