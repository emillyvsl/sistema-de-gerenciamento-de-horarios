from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.semestre import Semestre
from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.preferencias import Preferencias  # Importar Preferencias

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
    dias_semana = DiasSemana.objects.all()
    pesquisa_realizada = False

    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso
    ).select_related(
        'disciplina',
        'ano_semestre',
        'horario_curso'
    ).prefetch_related(
        'disciplina__disciplina_professores__professor',
        'horario_curso__dias_semana',
        'disciplina__disciplina_professores__professor__preferencias'
    )

    if ano and semestre_id:
        horarios = horarios.filter(ano_semestre__ano=ano, ano_semestre__semestre_id=semestre_id)
        pesquisa_realizada = True
    else:
        try:
            ultimo_ano_semestre = AnoSemestre.objects.filter(curso=curso).latest('ano', 'semestre')
            horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
            messages.warning(request, "Para pesquisar, selecione o ano e o semestre. Exibindo o quadro mais recente.")
        except AnoSemestre.DoesNotExist:
            horarios = None
            messages.warning(request, "Nenhum ano/semestre encontrado.")

    # Processa horários únicos e insere placeholders para horários sem alocações
    horarios_unicos = []
    horarios_vistos = set()

    if horarios:
        for horario in horarios:
            chave_horario = (
                horario.horario_curso.hora_inicio,
                horario.horario_curso.hora_fim,
                horario.periodo,
                tuple(dia.nome for dia in horario.horario_curso.dias_semana.all())
            )

            if chave_horario not in horarios_vistos:
                horarios_vistos.add(chave_horario)
                horarios_unicos.append(horario)

                # Inclui placeholders para manter a linha visível, mesmo sem alocações
                alocacoes = HorariosDisciplinas.objects.filter(
                    horario_curso=horario.horario_curso,
                    ano_semestre=horario.ano_semestre,
                    periodo=horario.periodo
                ).select_related('disciplina', 'dia_semana')

                # Adiciona lista vazia se não houver alocações para o horário específico
                horario.alocacoes_list = alocacoes if alocacoes.exists() else [{'disciplina': None}]

    colspan_value = len(dias_semana) + 2
    preferencias_professores = Preferencias.objects.all()

    context = {
        'horarios': horarios_unicos,
        'semestres': semestres,
        'pesquisa_realizada': pesquisa_realizada,
        'dias_semana': dias_semana,
        'colspan_value': colspan_value,
        'preferencias_professores': preferencias_professores,
    }

    return render(request, 'horarios/horarios_disciplinas.html', context)

@login_required
def remover_alocacao(request, alocacao_id):
    # Obter a alocação específica ou retornar 404 se não existir
    alocacao = get_object_or_404(HorariosDisciplinas, id=alocacao_id)

    if request.method == 'POST':
        # Remove a alocação do banco de dados
        alocacao.delete()
        
        # Exibir uma mensagem de sucesso para o usuário
        messages.success(request, 'Alocação removida com sucesso.')

        # Redirecionar de volta para a página de horários
        return redirect('horarios_disciplinas')
    
    # Se a solicitação não for POST, exibe uma mensagem de erro
    messages.error(request, 'Método de requisição inválido.')
    return redirect('horarios_disciplinas')