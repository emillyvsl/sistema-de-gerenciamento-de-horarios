from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models import dias_semana
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
    periodo_escolhido = request.GET.get('periodo')  # Capturando o período escolhido

    # Inicializar horários com os horários relacionados ao curso
    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso
    ).select_related(
        'disciplina_professor__disciplina',
        'disciplina_professor__professor',
        'ano_semestre',
        'horario_curso'
    ).prefetch_related('horario_curso__dias_semana')

    # Verificando se ambos ano e semestre foram selecionados
    if ano and semestre_id:
        horarios = horarios.filter(ano_semestre__ano=ano, ano_semestre__semestre_id=semestre_id)

        # Filtrar períodos pares ou ímpares, dependendo da escolha do usuário
        if periodo_escolhido == 'par':
            horarios = horarios.filter(periodo__in=[p for p in range(2, curso.numero_periodos + 1, 2)])
        elif periodo_escolhido == 'impar':
            horarios = horarios.filter(periodo__in=[p for p in range(1, curso.numero_periodos + 1, 2)])

        pesquisa_realizada = True  # Pesquisa foi realizada
    else:
        # Caso não haja filtros, pegar o quadro mais recente
        ultimo_ano_semestre = AnoSemestre.objects.latest('ano', 'semestre')
        horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
        pesquisa_realizada = False  # Não foi realizada pesquisa

        # Mensagem para informar que o quadro mais recente está sendo exibido
        messages.warning(request, "Para pesquisar deve ser selecionado o ano e o semestre. Exibindo o quadro mais recente.")

    context = {
        'horarios': horarios,
        'semestres': semestres,
        'pesquisa_realizada': pesquisa_realizada,
        'dias_semana': dias_semana,  # Passando dias da semana para o template
    }

    return render(request, 'horarios/horarios_disciplinas.html', context)
