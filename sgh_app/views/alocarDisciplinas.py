from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from sgh_app.models import DiasSemana, HorariosDisciplinas, DisciplinaProfessor, HorarioCurso, AnoSemestre

@login_required
def alocarDisciplina(request, horario_id, dia_id):
    try:
        horario = get_object_or_404(HorarioCurso, id=horario_id)
    except HorarioCurso.DoesNotExist:
        return JsonResponse({'success': False, 'message': f'Horário com ID {horario_id} não encontrado.'}, status=404)

    try:
        
        dia_semana = get_object_or_404(DiasSemana, id=dia_id)
    except DiasSemana.DoesNotExist:
        return JsonResponse({'success': False, 'message': f'Dia da semana com ID {dia_id} não encontrado.'}, status=404)
    print(f"Horario ID: {horario_id}, Dia ID: {dia_id}")

    if request.method == 'GET':
        disciplinas_professores = DisciplinaProfessor.objects.all()

        context = {
            'horario': horario,
            'dia': dia_semana,
            'disciplinas_professores': disciplinas_professores,
        }
        return render(request, 'horarios/alocar_disciplina.html', context)

    elif request.method == 'POST':
        print("Dados recebidos na requisição POST:", request.POST)
        disciplina_professor_id = request.POST.get('disciplina_professor_id')
        ano_semestre_id = request.GET.get('ano_semestre_id')  # Obtém o ID do ano e semestre da URL
        
        # Verifique se o ID de AnoSemestre foi fornecido
        if not ano_semestre_id:
            return JsonResponse({'success': False, 'message': 'ID de ano semestre não foi fornecido.'}, status=400)
        
        # Tente obter o objeto AnoSemestre
        ano_semestre = get_object_or_404(AnoSemestre, id=ano_semestre_id)

        # Verifique se o ID da DisciplinaProfessor foi enviado
        if not disciplina_professor_id:
            return JsonResponse({'success': False, 'message': 'ID de disciplina professor não foi fornecido.'}, status=400)

        disciplina_professor = get_object_or_404(DisciplinaProfessor, id=disciplina_professor_id)

        try:
            # Crie uma nova alocação de disciplina
            HorariosDisciplinas.objects.create(
                disciplina_professor=disciplina_professor,
                horario_curso=horario,
                ano_semestre=ano_semestre,  # Agora associando corretamente com o ano e semestre
                periodo=horario.periodo  # Usando o período já existente
            )
            return JsonResponse({'success': True, 'message': 'Disciplina alocada com sucesso!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao alocar disciplina: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método não permitido!'}, status=405)

