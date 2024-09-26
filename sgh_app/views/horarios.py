from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horario_curso import HorarioCurso
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist


@login_required
def horarios_curso(request):
    return render(request, 'horarios/horario_curso.html')

def horarios_adicionar(request):
    # Obtendo o curso a partir da coordenação do usuário logado
    coordenacao = request.user.coordenacao
    curso = coordenacao.curso

    # Se for uma requisição POST, processamos o formulário
    if request.method == 'POST':
        dias_ids = request.POST.getlist('dias_semana')
        hora_inicio = request.POST['hora_inicio']
        hora_fim = request.POST['hora_fim']
        
        # Obtém os objetos DiasSemana pelos IDs selecionados
        dias = DiasSemana.objects.filter(id__in=dias_ids)
        
        # Cria um novo HorarioCurso associado ao curso do coordenador
        novo_horario = HorarioCurso.objects.create(
            curso=curso,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        
        # Adiciona os dias da semana selecionados
        novo_horario.dias_semana.set(dias)
        novo_horario.save()

        return redirect('horarios_adicionar')

    # Para requisições GET, renderizamos a tabela com horários
    dias = DiasSemana.objects.all()
    horarios_curso = HorarioCurso.objects.filter(curso=curso)

    # Organizando horários por dia da semana
    horarios_por_dia = defaultdict(list)
    for horario in horarios_curso:
        for dia in horario.dias_semana.all():
            horarios_por_dia[dia.nome].append(horario)

    return render(request, 'horarios/horario_adicionar.html', {
        'dias': dias,
        'horarios_por_dia': dict(horarios_por_dia),
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
        horario.delete()
        messages.success(request, 'Horário removido com sucesso!')
        return redirect('horarios_adicionar')  # Redireciona para a lista de horários
