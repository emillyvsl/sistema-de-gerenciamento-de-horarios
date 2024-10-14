from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from sgh_app.models import DiasSemana, HorariosDisciplinas, DisciplinaProfessor, HorarioCurso, AnoSemestre

@login_required
def alocarDisciplina(request, horario_id, dia_id):
    # Tenta obter o HorarioCurso e o DiaSemana
    horario = get_object_or_404(HorarioCurso, id=horario_id)
    dia_semana = get_object_or_404(DiasSemana, id=dia_id)

    if request.method == 'GET':
        disciplinas_professores = DisciplinaProfessor.objects.all()
        try:
            hor_disc = HorariosDisciplinas.objects.filter(horario_curso=horario).latest('ano_semestre')
            ano_semestre_id = hor_disc.ano_semestre.id
            periodo = hor_disc.periodo
        except HorariosDisciplinas.DoesNotExist:
            ano_semestre_id = None
            periodo = None

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

        ano_semestre = get_object_or_404(AnoSemestre, id=ano_semestre_id)
        disciplina_professor = get_object_or_404(DisciplinaProfessor, id=disciplina_professor_id)

        periodo = request.POST.get('periodo')
        if not periodo:
            try:
                hor_disc = HorariosDisciplinas.objects.filter(horario_curso=horario).latest('ano_semestre')
                periodo = hor_disc.periodo
            except HorariosDisciplinas.DoesNotExist:
                periodo = 'impar'

        try:
            HorariosDisciplinas.objects.create(
                disciplina_professor=disciplina_professor,
                horario_curso=horario,
                ano_semestre=ano_semestre,
                periodo=periodo,
                dia_semana=dia_semana  # Adicionando o dia_semana na alocação
            )
            return HttpResponseRedirect(reverse('horarios_disciplinas'))
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao alocar disciplina: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Método não permitido!'}, status=405)
