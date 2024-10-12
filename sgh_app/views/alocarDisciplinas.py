# views.py

from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from sgh_app.models.alocacao_disciplinas import AlocacaoDisciplinas
from sgh_app.models.disciplina_professor import DisciplinaProfessor
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from django.contrib.auth.decorators import login_required


@login_required
def alocarDisciplina(request, horario_id, dia_id):
    if request.method == 'POST':
        disciplina_professor_id = request.POST.get('disciplina_professor')
        horario_id = request.POST.get('horario_id')
        dia_id = request.POST.get('dia_id')

        disciplina_professor = get_object_or_404(DisciplinaProfessor, id=disciplina_professor_id)
        horarios_disciplinas = get_object_or_404(HorariosDisciplinas, id=horario_id)

        # Verificando conflitos de alocação
        if AlocacaoDisciplinas.objects.filter(horarios_disciplinas=horarios_disciplinas, disciplina_professor=disciplina_professor).exists():
            return JsonResponse({'success': False, 'message': "Essa disciplina já está alocada para este horário."})

        # Criar nova alocação
        AlocacaoDisciplinas.objects.create(horarios_disciplinas=horarios_disciplinas, disciplina_professor=disciplina_professor)
        return JsonResponse({'success': True, 'message': f"Disciplina '{disciplina_professor.disciplina.nome}' alocada com sucesso para o dia {dia_id}!"})

    return JsonResponse({'success': False, 'message': "Método não permitido."})
