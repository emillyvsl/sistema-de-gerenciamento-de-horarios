from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.semestre import Semestre
from sgh_app.models.ano_semestre import AnoSemestre


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models import DiasSemana, HorariosDisciplinas, Semestre, AnoSemestre

@login_required
def horarioDisciplina(request):
    coordenacao = request.user.coordenacao

    if not coordenacao:
        messages.error(request, "Acesso negado: você não possui coordenação associada.")
        return redirect('home')

    curso = coordenacao.curso
    semestres = Semestre.objects.all()

    ano = request.GET.get('ano')
    semestre_id = request.GET.get('semestre')
    periodo_escolhido = request.GET.get('periodo')

    dias_semana = DiasSemana.objects.all()

    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso
    ).select_related(
        'disciplina_professor__disciplina',
        'disciplina_professor__professor',
        'ano_semestre',
        'horario_curso'
    ).prefetch_related('horario_curso__dias_semana')

    if ano and semestre_id:
        horarios = horarios.filter(ano_semestre__ano=ano, ano_semestre__semestre_id=semestre_id)
        pesquisa_realizada = True
    else:
        try:
            ultimo_ano_semestre = AnoSemestre.objects.latest('ano', 'semestre')
            horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
            pesquisa_realizada = False
            messages.warning(request, "Para pesquisar deve ser selecionado o ano e o semestre. Exibindo o quadro mais recente.")
        except AnoSemestre.DoesNotExist:
            horarios = None
            messages.warning(request, "Nenhum ano/semestre foi encontrado.")

    # Calcular o valor de colspan
    colspan_value = dias_semana.count() + 3

    context = {
        'horarios': horarios,
        'semestres': semestres,
        'pesquisa_realizada': pesquisa_realizada,
        'dias_semana': dias_semana,
        'colspan_value': colspan_value  # Passar o valor calculado para o template
    }

    return render(request, 'horarios/horarios_disciplinas.html', context)
