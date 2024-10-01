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

    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso
    ).select_related(
        'disciplina_professor__disciplina',
        'disciplina_professor__professor',
        'ano_semestre'
    )

    if ano:
        horarios = horarios.filter(ano_semestre__ano=ano)

    if semestre_id:
        horarios = horarios.filter(ano_semestre__semestre_id=semestre_id)

    # Obter os anos e semestres disponíveis para exibir
    anos_semestres = HorarioCurso.objects.filter(curso=curso).distinct()

    # Variável que indica se a pesquisa foi realizada
    pesquisa_realizada = bool(ano or semestre_id)

    context = {
        'anos_semestres': anos_semestres,
        'horarios': horarios,
        'semestres': semestres,  # Envia os semestres para o template
        'pesquisa_realizada': pesquisa_realizada,  # Nova variável
    }

    return render(request, 'horarios/horarios_disciplinas.html', context)
