from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from sgh_app.models import DiasSemana, HorariosDisciplinas, DisciplinaProfessor, HorarioCurso, AnoSemestre

@login_required
def alocarDisciplina(request, horario_id, dia_id, periodo_id):
    # Obter HorarioCurso, DiaSemana e verificar o período específico
    horario = get_object_or_404(HorarioCurso, id=horario_id)
    dia_semana = get_object_or_404(DiasSemana, id=dia_id)
    periodo = periodo_id  # Recebe o período numérico diretamente

    if request.method == 'GET':
        disciplinas_professores = DisciplinaProfessor.objects.all()
        try:
            # Buscar a alocação existente para o horário, dia, e período
            hor_disc = HorariosDisciplinas.objects.filter(
                horario_curso=horario, dia_semana=dia_semana, periodo=periodo
            ).latest('ano_semestre')
            ano_semestre_id = hor_disc.ano_semestre.id
        except HorariosDisciplinas.DoesNotExist:
            # Tentar buscar o ano/semestre mais recente se não houver alocação
            try:
                ano_semestre = AnoSemestre.objects.latest('id')
                ano_semestre_id = ano_semestre.id
            except AnoSemestre.DoesNotExist:
                # Se não houver AnoSemestre registrado
                ano_semestre_id = None

        context = {
            'horario': horario,  # Corrigindo o objeto passado
            'dia': dia_semana,
            'disciplinas_professores': disciplinas_professores,
            'ano_semestre_id': ano_semestre_id,
            'periodo': periodo,  # O período numérico é passado para o template
        }

        return render(request, 'horarios/alocar_disciplina.html', context)

    elif request.method == 'POST':
        disciplina_professor_id = request.POST.get('disciplina_professor')
        ano_semestre_id = request.POST.get('ano_semestre_id')

        # Garantir que estamos alocando para o ano/semestre e disciplina corretos
        ano_semestre = get_object_or_404(AnoSemestre, id=ano_semestre_id)
        disciplina_professor = get_object_or_404(DisciplinaProfessor, id=disciplina_professor_id)

        try:
            # Verificar se já existe uma alocação para o mesmo horário, dia, período e ano/semestre
            alocacao_existente = HorariosDisciplinas.objects.filter(
                horario_curso=horario,  # Certificando que o objeto correto está sendo utilizado
                dia_semana=dia_semana,
                periodo=periodo,
                ano_semestre=ano_semestre
            ).exists()

            if not alocacao_existente:
                # Cria a alocação de disciplina para o horário, dia e período corretos
                HorariosDisciplinas.objects.create(
                    disciplina_professor=disciplina_professor,
                    horario_curso=horario,
                    ano_semestre=ano_semestre,
                    periodo=periodo,
                    dia_semana=dia_semana
                )
            return HttpResponseRedirect(reverse('horarios_disciplinas'))
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao alocar disciplina: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Método não permitido!'}, status=405)
