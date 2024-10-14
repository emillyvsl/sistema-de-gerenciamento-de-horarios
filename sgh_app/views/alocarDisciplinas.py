from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from sgh_app.models import DiasSemana, HorariosDisciplinas, DisciplinaProfessor, HorarioCurso, AnoSemestre

@login_required
def alocarDisciplina(request, horario_id, dia_id):
    # Tenta obter o HorarioCurso
    horario = get_object_or_404(HorarioCurso, id=horario_id)
    
    # Tenta obter o DiaSemana
    dia_semana = get_object_or_404(DiasSemana, id=dia_id)
    
    print(f"Horario ID: {horario_id}, Dia ID: {dia_id}")

    if request.method == 'GET':
        disciplinas_professores = DisciplinaProfessor.objects.all()

        # Encontrar o ano_semestre_id mais recente para este horario_curso
        try:
            hor_disc = HorariosDisciplinas.objects.filter(horario_curso=horario).latest('ano_semestre')
            ano_semestre_id = hor_disc.ano_semestre.id
            periodo = hor_disc.periodo  # Obter o período da alocação existente
        except HorariosDisciplinas.DoesNotExist:
            ano_semestre_id = None
            periodo = None  # Defina o valor padrão se não for encontrado

        print(f"Ano Semestre ID encontrado: {ano_semestre_id}, Período encontrado: {periodo}")

        context = {
            'horario': horario,
            'dia': dia_semana,
            'disciplinas_professores': disciplinas_professores,
            'ano_semestre_id': ano_semestre_id,
            'periodo': periodo,
        }
        return render(request, 'horarios/alocar_disciplina.html', context)

    elif request.method == 'POST':
        print("Dados recebidos na requisição POST:", request.POST)
        disciplina_professor_id = request.POST.get('disciplina_professor')
        ano_semestre_id = request.POST.get('ano_semestre_id')

        # Verifique se o ID de AnoSemestre foi fornecido
        if not ano_semestre_id:
            return JsonResponse({'success': False, 'message': 'ID de ano semestre não foi fornecido.'}, status=400)

        # Tente obter o objeto AnoSemestre
        ano_semestre = get_object_or_404(AnoSemestre, id=ano_semestre_id)

        # Verifique se o ID da DisciplinaProfessor foi enviado
        if not disciplina_professor_id:
            return JsonResponse({'success': False, 'message': 'ID de disciplina professor não foi fornecido.'}, status=400)

        disciplina_professor = get_object_or_404(DisciplinaProfessor, id=disciplina_professor_id)

        # Verifique se o período foi obtido corretamente
        periodo = request.POST.get('periodo')
        if not periodo:
            # Caso o período não esteja no POST, busque novamente
            try:
                hor_disc = HorariosDisciplinas.objects.filter(horario_curso=horario).latest('ano_semestre')
                periodo = hor_disc.periodo
            except HorariosDisciplinas.DoesNotExist:
                periodo = 'impar'  # Defina um valor padrão

        try:
            # Crie uma nova alocação de disciplina
            HorariosDisciplinas.objects.create(
                disciplina_professor=disciplina_professor,
                horario_curso=horario,
                ano_semestre=ano_semestre,
                periodo=periodo  # Usando o período obtido
            )
            return JsonResponse({'success': True, 'message': 'Disciplina alocada com sucesso!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao alocar disciplina: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Método não permitido!'}, status=405)
