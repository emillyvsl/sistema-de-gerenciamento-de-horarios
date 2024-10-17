from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from sgh_app.models import DiasSemana, HorariosDisciplinas, DisciplinaProfessor, HorarioCurso, AnoSemestre

@login_required
def alocarDisciplina(request, horario_id, dia_id, periodo_id):
    print(f"Dia ID: {dia_id}, Horario ID: {horario_id}, Periodo ID: {periodo_id}")
    print(f"Dados POST: {request.POST}")

    # Obter HorarioCurso, DiaSemana e verificar o período específico
    horario = get_object_or_404(HorarioCurso, id=horario_id)
    dia_semana = get_object_or_404(DiasSemana, id=dia_id)
    periodo = periodo_id  # Recebe o período numérico diretamente

    # Depuração para verificar se os objetos foram carregados corretamente
    print(f"Horario: {horario}")
    print(f"Dia da semana: {dia_semana}")
    print(f"Período: {periodo}")

    if request.method == 'GET':
        disciplinas_professores = DisciplinaProfessor.objects.all()
        try:
            # Buscar a alocação existente para o horário, dia, e período
            hor_disc = HorariosDisciplinas.objects.filter(
                horario_curso=horario, dia_semana=dia_semana, periodo=periodo
            ).latest('ano_semestre')
            ano_semestre_id = hor_disc.ano_semestre.id
            print(f"Alocação encontrada. Ano Semestre ID: {ano_semestre_id}")
        except HorariosDisciplinas.DoesNotExist:
            # Tentar buscar o ano/semestre mais recente se não houver alocação
            try:
                ano_semestre = AnoSemestre.objects.latest('id')
                ano_semestre_id = ano_semestre.id
                print(f"Nenhuma alocação existente. Usando Ano Semestre ID mais recente: {ano_semestre_id}")
            except AnoSemestre.DoesNotExist:
                # Se não houver AnoSemestre registrado
                ano_semestre_id = None
                print("Nenhum AnoSemestre encontrado.")

        context = {
            'horario': horario,
            'dia': dia_semana,
            'disciplinas_professores': disciplinas_professores,
            'ano_semestre_id': ano_semestre_id,
            'periodo': periodo,
        }

        return render(request, 'horarios/alocar_disciplina.html', context)

    elif request.method == 'POST':
        disciplina_professor_id = request.POST.get('disciplina_professor')
        ano_semestre_id = request.POST.get('ano_semestre_id')

        # Logs para depuração
        print(f"Tentando alocar disciplina para {dia_semana.nome} no período {periodo}")
        print(f"Disciplina Professor ID: {disciplina_professor_id}")
        print(f"Ano Semestre ID: {ano_semestre_id}")
        print(f"Periodo: {periodo}")

        # Garantir que estamos alocando para o ano/semestre e disciplina corretos
        disciplina_professor = get_object_or_404(DisciplinaProfessor, id=disciplina_professor_id)
        ano_semestre = get_object_or_404(AnoSemestre, id=ano_semestre_id)

        try:
            # Verificar se o professor já está alocado no mesmo horário, dia e ano/semestre
            conflito_alocacao = HorariosDisciplinas.objects.filter(
                disciplina_professor__professor=disciplina_professor.professor,
                horario_curso__hora_inicio=horario.hora_inicio,
                horario_curso__hora_fim=horario.hora_fim,
                dia_semana=dia_semana,
                ano_semestre=ano_semestre
            ).exists()

            if conflito_alocacao:
                # Se já existir uma alocação para o professor no mesmo horário, dia e ano/semestre, impedir a criação
                messages.error(request, f"O professor {disciplina_professor.professor.nome} já está alocado no mesmo dia e horário.")
                return HttpResponseRedirect(reverse('horarios_disciplinas'))

            # Verificar se já existe uma alocação no mesmo dia, horário e período (independentemente do professor)
            alocacao_existente = HorariosDisciplinas.objects.filter(
                horario_curso=horario,
                dia_semana=dia_semana,
                periodo=periodo,
                ano_semestre=ano_semestre
            ).exclude(disciplina_professor=None).exists()

            if alocacao_existente:
                # Impedir a criação se já existir uma alocação para aquele dia, horário e período
                messages.error(request, f"Já existe uma alocação para o dia {dia_semana.nome}, horário {horario.hora_inicio}-{horario.hora_fim} e período {periodo}.")
                return HttpResponseRedirect(reverse('horarios_disciplinas'))

            # Verificar se já existe uma alocação sem professor
            alocacao_sem_professor = HorariosDisciplinas.objects.filter(
                horario_curso=horario,
                dia_semana=dia_semana,
                periodo=periodo,
                ano_semestre=ano_semestre
            ).first()

            if alocacao_sem_professor and alocacao_sem_professor.disciplina_professor is None:
                # Atualiza a alocação existente com o professor selecionado
                alocacao_sem_professor.disciplina_professor = disciplina_professor
                alocacao_sem_professor.save()
                print(f"Alocação atualizada: {alocacao_sem_professor}")
                messages.success(request, 'Alocação atualizada com sucesso.')
            elif not alocacao_sem_professor:
                # Cria uma nova alocação se não houver uma alocação existente
                nova_alocacao = HorariosDisciplinas.objects.create(
                    disciplina_professor=disciplina_professor,
                    horario_curso=horario,
                    ano_semestre=ano_semestre,
                    periodo=periodo,
                    dia_semana=dia_semana
                )
                print(f"Nova alocação criada: {nova_alocacao}")
                messages.success(request, 'Nova alocação criada com sucesso.')
            else:
                print("Alocação já existente.")
                messages.warning(request, 'Alocação já existente.')

            return HttpResponseRedirect(reverse('horarios_disciplinas'))

        except Exception as e:
            print(f"Erro ao salvar alocação para {dia_semana.nome} no período {periodo}. Detalhes do erro: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Erro ao alocar disciplina: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Método não permitido!'}, status=405)
