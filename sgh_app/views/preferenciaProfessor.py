# sgh_app/views/preferencia_professor.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.preferencias import Preferencias
from sgh_app.models.professor import Professor

def adicionar_preferencia_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)

    if request.method == "POST":
        dias_preferidos_ids = request.POST.getlist('dias_preferidos')  # Múltiplos valores podem ser retornados
        horas_preferidas_ids = request.POST.getlist('horas_preferidas')  # Múltiplos valores podem ser retornados

        preferencia = Preferencias(professor=professor)
        preferencia.save()

        # Associar os dias e horários selecionados
        preferencia.dias_preferidos.set(DiasSemana.objects.filter(id__in=dias_preferidos_ids))
        preferencia.horas_preferidas.set(HorarioCurso.objects.filter(id__in=horas_preferidas_ids))

        preferencia.save()

        messages.success(request, 'Preferência de horário adicionada com sucesso!')
        return redirect('detalhes_professor', professor_id=professor.id)  # Redirecionar para detalhes do professor

    return redirect('detalhes_professor', professor_id=professor.id)  # Também redirecionar para detalhes do professor se não for POST


def remover_preferencia_professor(request, preferencia_id, professor_id):
    preferencia = get_object_or_404(Preferencias, id=preferencia_id)
    
    if preferencia.professor.id != professor_id:
        messages.error(request, 'Preferência não encontrada.')
        return redirect('detalhes_professor', professor_id=professor_id)

    preferencia.delete()
    messages.success(request, 'Preferência removida com sucesso!')
    return redirect('detalhes_professor', professor_id=professor_id)
