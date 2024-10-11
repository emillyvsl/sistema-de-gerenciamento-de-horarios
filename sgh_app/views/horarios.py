from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horario_curso import HorarioCurso
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist

from sgh_app.models.horarios_disciplinas import HorariosDisciplinas


@login_required
def horarios_curso(request):
    return render(request, 'horarios/horario_curso.html')

@login_required
def horarios_adicionar(request):
    coordenacao = request.user.coordenacao
    curso = coordenacao.curso

    if request.method == 'POST':
        dias_ids = request.POST.getlist('dias_semana')
        hora_inicio = request.POST['hora_inicio']
        hora_fim = request.POST['hora_fim']
        
        # Obtenha os dias selecionados
        dias = DiasSemana.objects.filter(id__in=dias_ids)

        # Obtenha o ano e semestre atual
        try:
            ano_semestre = AnoSemestre.objects.latest('ano', 'semestre')
        except ObjectDoesNotExist:
            messages.error(request, 'Ano e semestre não definidos.')
            return redirect('horarios_adicionar')

        # Crie um único horário para todos os dias selecionados
        novo_horario = HorarioCurso.objects.create(
            curso=curso,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )

        # Associe os dias selecionados ao novo horário
        novo_horario.dias_semana.set(dias)  # Associa todos os dias de uma vez
        novo_horario.save()

        # Cria uma nova entrada em HorariosDisciplinas associada ao HorarioCurso e AnoSemestre
        HorariosDisciplinas.objects.create(
            horario_curso=novo_horario,
            ano_semestre=ano_semestre,
            disciplina_professor=None  # Você pode definir isso depois se necessário
        )

        messages.success(request, 'Horários e quadro de horários adicionados com sucesso!')
        return redirect('horarios_adicionar')

    dias = DiasSemana.objects.all()
    horarios_curso = HorarioCurso.objects.filter(curso=curso)

    return render(request, 'horarios/horario_adicionar.html', {
        'dias': dias,
        'horarios_curso': horarios_curso,
        'curso': curso
    })



@login_required
def horarios_editar(request, horario_id):
    horario = get_object_or_404(HorarioCurso, id=horario_id)

    if request.method == 'POST':
        horario.hora_inicio = request.POST['hora_inicio']
        horario.hora_fim = request.POST['hora_fim']
        horario.save()
        messages.success(request, 'Horário editado com sucesso!')
        return redirect('horarios_adicionar')  # Redireciona para a lista de horários


@login_required
def horarios_excluir(request, horario_id):
    horario = get_object_or_404(HorarioCurso, id=horario_id)
    
    if request.method == 'POST':
        # Remover as entradas em HorariosDisciplinas associadas a esse HorarioCurso
        HorariosDisciplinas.objects.filter(horario_curso=horario).delete()
        
        # Excluir o HorarioCurso
        horario.delete()

        messages.success(request, 'Horário e quadro de horários removidos com sucesso!')
        return redirect('horarios_adicionar')

