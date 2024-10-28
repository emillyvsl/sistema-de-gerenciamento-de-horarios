from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from sgh_app.models import DiasSemana, HorariosDisciplinas, Disciplina, HorarioCurso, AnoSemestre, DisciplinaProfessor

@login_required
def alocarDisciplina(request, horario_id, dia_id, periodo_id):
    user = request.user
    coordenacao = user.coordenacao

    if not coordenacao:
        messages.error(request, "Você não possui coordenação associada.")
        return redirect('horarios_disciplinas')

    curso = coordenacao.curso
    horario = get_object_or_404(HorarioCurso, id=horario_id)
    dia_semana = get_object_or_404(DiasSemana, id=dia_id)
    periodo = periodo_id

    if request.method == 'GET':
        # Filtrar disciplinas relacionadas ao curso e com professores associados
        disciplinas_com_professores = Disciplina.objects.filter(
            curso=curso, disciplina_professores__isnull=False
        ).distinct()

        try:
            hor_disc = HorariosDisciplinas.objects.filter(
                horario_curso=horario, dia_semana=dia_semana, periodo=periodo
            ).latest('ano_semestre')
            ano_semestre_id = hor_disc.ano_semestre.id
        except HorariosDisciplinas.DoesNotExist:
            try:
                ano_semestre = AnoSemestre.objects.latest('id')
                ano_semestre_id = ano_semestre.id
            except AnoSemestre.DoesNotExist:
                ano_semestre_id = None

        context = {
            'horario': horario,
            'dia': dia_semana,
            'disciplinas': disciplinas_com_professores,
            'ano_semestre_id': ano_semestre_id,
            'periodo': periodo,
        }

        return render(request, 'horarios/alocar_disciplina.html', context)

    elif request.method == 'POST':
        disciplina_id = request.POST.get('disciplina')
        ano_semestre_id = request.POST.get('ano_semestre_id')

        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        ano_semestre = get_object_or_404(AnoSemestre, id=ano_semestre_id)

        # Verificar se a disciplina tem um professor associado
        if not DisciplinaProfessor.objects.filter(disciplina=disciplina).exists():
            messages.error(request, f"A disciplina {disciplina.nome} não possui professores associados.")
            return HttpResponseRedirect(reverse('horarios_disciplinas'))

        try:
            # Verifica se a disciplina já está alocada no mesmo dia e horário em qualquer período
            conflito_disciplina = HorariosDisciplinas.objects.filter(
                disciplina=disciplina,
                dia_semana=dia_semana,
                horario_curso__hora_inicio=horario.hora_inicio,
                horario_curso__hora_fim=horario.hora_fim,
                ano_semestre=ano_semestre
            ).exists()

            if conflito_disciplina:
                messages.error(request, f"A disciplina {disciplina.nome} já está alocada no dia {dia_semana.nome} no horário {horario.hora_inicio}-{horario.hora_fim} em outro período.")
                return HttpResponseRedirect(reverse('horarios_disciplinas'))

            # Verifica se já existe uma alocação no horário, dia, período e ano_semestre
            alocacao_existente = HorariosDisciplinas.objects.filter(
                horario_curso=horario,
                dia_semana=dia_semana,
                periodo=periodo,
                ano_semestre=ano_semestre
            ).first()

            if alocacao_existente:
                if alocacao_existente.disciplina is None:
                    alocacao_existente.disciplina = disciplina
                    alocacao_existente.save()
                    messages.success(request, 'Alocação atualizada com sucesso.')
                else:
                    messages.error(request, f"Já existe uma alocação para a disciplina {alocacao_existente.disciplina.nome} no dia {dia_semana.nome}, horário {horario.hora_inicio}-{horario.hora_fim} e período {periodo}.")
                return HttpResponseRedirect(reverse('horarios_disciplinas'))
            else:
                nova_alocacao = HorariosDisciplinas.objects.create(
                    disciplina=disciplina,
                    horario_curso=horario,
                    ano_semestre=ano_semestre,
                    periodo=periodo,
                    dia_semana=dia_semana
                )
                messages.success(request, 'Nova alocação criada com sucesso.')

            return HttpResponseRedirect(reverse('horarios_disciplinas'))

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao alocar disciplina: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Método não permitido!'}, status=405)
