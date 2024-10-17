from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.disciplina_professor import DisciplinaProfessor
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
    semestres = Semestre.objects.all()

    ano = request.GET.get('ano')
    semestre_id = request.GET.get('semestre')

    dias_semana = DiasSemana.objects.all()
    pesquisa_realizada = False

    # Obter os horários filtrados pelo curso e ano/semestre
    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso  # Filtrar pelo curso atual
    ).select_related(
        'disciplina_professor__disciplina',
        'disciplina_professor__professor',
        'ano_semestre',
        'horario_curso'
    ).prefetch_related('horario_curso__dias_semana')

    if ano and semestre_id:
        # Filtrar pelos parâmetros ano e semestre fornecidos pelo usuário
        horarios = horarios.filter(ano_semestre__ano=ano, ano_semestre__semestre_id=semestre_id)
        pesquisa_realizada = True
    else:
        try:
            # Se o ano e semestre não forem fornecidos, buscar o mais recente
            ultimo_ano_semestre = AnoSemestre.objects.filter(curso=curso).latest('ano', 'semestre')
            horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
            messages.warning(request, "Para pesquisar deve ser selecionado o ano e o semestre. Exibindo o quadro mais recente.")
        except AnoSemestre.DoesNotExist:
            horarios = None
            messages.warning(request, "Nenhum ano/semestre foi encontrado.")

    # Garantir que apenas horários únicos sejam adicionados
    horarios_unicos = []
    horarios_vistos = set()

    if horarios:
        for horario in horarios:
            # Criar uma chave única baseada em período, horário e dias da semana
            chave_horario = (
                horario.horario_curso.hora_inicio,
                horario.horario_curso.hora_fim,
                horario.periodo,
                tuple(dia.nome for dia in horario.horario_curso.dias_semana.all())
            )

            # Verificar se essa chave já foi vista; caso contrário, adicioná-la
            if chave_horario not in horarios_vistos:
                horarios_vistos.add(chave_horario)
                horarios_unicos.append(horario)

                # Adicionar todas as alocações correspondentes ao horário, dia e ano_semestre
                alocacoes = HorariosDisciplinas.objects.filter(
                    horario_curso=horario.horario_curso,
                    ano_semestre=horario.ano_semestre  # Certificar-se de que o ano_semestre é filtrado corretamente
                )
                horario.alocacoes_list = alocacoes  # Passa todas as alocações desse horário

    colspan_value = len(dias_semana) + 2  # Calcular o valor do colspan para a tabela

    context = {
        'horarios': horarios_unicos,
        'semestres': semestres,
        'pesquisa_realizada': pesquisa_realizada,
        'dias_semana': dias_semana,
        'colspan_value': colspan_value,
    }

    return render(request, 'horarios/horarios_disciplinas.html', context)
