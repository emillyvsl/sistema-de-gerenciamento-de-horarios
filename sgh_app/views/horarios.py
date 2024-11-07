import json
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
from datetime import time

from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.preferencias import Preferencias


@login_required
def horarios_curso(request):
    return render(request, "horarios/horario_curso.html")

@login_required
def horarios_adicionar(request):
    coordenacao = request.user.coordenacao
    curso = coordenacao.curso

    if request.method == "POST":
        dias_ids = request.POST.getlist("dias_semana")
        hora_inicio = time.fromisoformat(request.POST["hora_inicio"])
        hora_fim = time.fromisoformat(request.POST["hora_fim"])

        if not dias_ids:
            messages.error(
                request,
                "Erro ao adicionar horário, selecione pelo menos um dia da semana.",
            )
            return redirect("horarios_adicionar")

        if hora_fim <= hora_inicio:
            messages.error(
                request,
                "Erro ao adicionar horário, o horário de fim deve ser posterior ao horário de início.",
            )
            return redirect("horarios_adicionar")

        # Seleciona os dias da semana com base nos IDs fornecidos
        dias = DiasSemana.objects.filter(id__in=dias_ids)

        for dia in dias:
            horarios_existentes = HorarioCurso.objects.filter(
                curso=curso, dias_semana=dia, is_ativo=True  # Apenas horários ativos
            )
            for horario in horarios_existentes:
                if hora_inicio < horario.hora_fim and hora_fim > horario.hora_inicio:
                    messages.error(
                        request,
                        f"Erro ao adicionar horário, Conflito de horário: o intervalo {hora_inicio} - {hora_fim} já está ocupado no dia {dia.nome}.",
                    )
                    return redirect("horarios_adicionar")

        # Criação do novo horário do curso
        novo_horario = HorarioCurso.objects.create(
            curso=curso, hora_inicio=hora_inicio, hora_fim=hora_fim
        )
        novo_horario.dias_semana.set(dias)
        novo_horario.save()

        # Verificar e adicionar o novo horário ao AnoSemestre mais recente
        try:
            ultimo_ano_semestre = AnoSemestre.objects.filter(curso=curso).latest(
                "ano", "semestre"
            )
            dias_semana = DiasSemana.objects.filter(id__in=dias_ids)

            if ultimo_ano_semestre.semestre.nome == "primeiro_semestre":
                periodos_relevantes = [
                    i for i in range(1, curso.quantidade_periodos + 1) if i % 2 == 0
                ]
            else:
                periodos_relevantes = [
                    i for i in range(1, curso.quantidade_periodos + 1) if i % 2 != 0
                ]

            for periodo_num in periodos_relevantes:
                for dia in dias_semana:
                    if not HorariosDisciplinas.objects.filter(
                        horario_curso=novo_horario,
                        dia_semana=dia,
                        periodo=periodo_num,
                        ano_semestre=ultimo_ano_semestre,
                        curso=curso,
                    ).exists():
                        HorariosDisciplinas.objects.create(
                            horario_curso=novo_horario,
                            ano_semestre=ultimo_ano_semestre,
                            periodo=periodo_num,
                            dia_semana=dia,
                            curso=curso,
                            disciplina=None,
                        )

            messages.success(
                request, "Horários e quadro de horários adicionados com sucesso!"
            )
        except AnoSemestre.DoesNotExist:
            messages.warning(
                request,
                "Nenhum quadro de horários recente foi encontrado. O horário foi criado, mas não foi associado a nenhum quadro.",
            )

        return redirect("horarios_adicionar")

    dias = DiasSemana.objects.all()
    horarios_curso = HorarioCurso.objects.filter(
        curso=curso, is_ativo=True  # Apenas horários ativos
    )

    for horario in horarios_curso:
        horario.dias_semana_json = json.dumps(
            list(horario.dias_semana.values_list("id", flat=True))
        )

    return render(
        request,
        "horarios/horario_adicionar.html",
        {"dias": dias, "horarios_curso": horarios_curso, "curso": curso},
    )


@login_required
def horarios_editar(request, horario_id):
    horario = get_object_or_404(HorarioCurso, id=horario_id)
    curso = horario.curso  # Obter o curso associado ao horário

    if request.method == "POST":
        # Obtenha os novos valores de início e fim
        hora_inicio = time.fromisoformat(request.POST["hora_inicio"])
        hora_fim = time.fromisoformat(request.POST["hora_fim"])
        dias_ids = request.POST.getlist("dias_semana")

        # Verificação: não permitir que todos os dias sejam desmarcados
        if not dias_ids:
            messages.error(
                request,
                "Erro ao editar, o horário deve estar associado a pelo menos um dia da semana.",
            )
            return redirect("horarios_adicionar")

        # Verificação: horário de fim não pode ser anterior ao horário de início
        if hora_fim <= hora_inicio:
            messages.error(
                request,
                "Erro ao editar, o horário de fim deve ser posterior ao horário de início.",
            )
            return redirect("horarios_adicionar")

        dias = DiasSemana.objects.filter(id__in=dias_ids)

        # Verificar sobreposição de horário, ignorando o horário atual que está sendo editado
        for dia in dias:
            horarios_existentes = HorarioCurso.objects.filter(
                curso=curso, dias_semana=dia
            ).exclude(
                id=horario_id
            )  # Excluir o horário atual da verificação

            for horario_existente in horarios_existentes:
                # Verificar se o novo intervalo sobrepõe algum horário existente
                if (
                    hora_inicio < horario_existente.hora_fim
                    and hora_fim > horario_existente.hora_inicio
                ):
                    messages.error(
                        request,
                        f"Erro ao editar, Conflito de horário: o intervalo {hora_inicio} - {hora_fim} já está ocupado no dia {dia.nome}.",
                    )
                    return redirect("horarios_adicionar")

        # Se não houver conflitos, atualizar o horário existente
        horario.hora_inicio = hora_inicio
        horario.hora_fim = hora_fim
        horario.dias_semana.set(dias)
        horario.save()

        messages.success(request, "Horário editado com sucesso!")
        return redirect("horarios_adicionar")  # Redireciona para a lista de horários


@login_required
def horarios_excluir(request, horario_id):
    horario = get_object_or_404(HorarioCurso, id=horario_id)

    if request.method == "POST":
        # Marcar o HorarioCurso como inativo
        horario.is_ativo = False
        horario.save()

        # Remover as entradas de HorariosDisciplinas associadas ao último AnoSemestre
        try:
            ultimo_ano_semestre = AnoSemestre.objects.filter(curso=horario.curso).latest("ano", "semestre")
            HorariosDisciplinas.objects.filter(horario_curso=horario, ano_semestre=ultimo_ano_semestre).delete()
            messages.success(request, "Horário marcado como inativo e removido do quadro de horários mais recente com sucesso!")
        except AnoSemestre.DoesNotExist:
            messages.warning(request, "Nenhum quadro de horários recente foi encontrado para remover o horário.")

        return redirect("horarios_adicionar")

    messages.warning(request, "Ao inativar este horário, ele não estará mais disponível.")
    return render(request, "horarios/confirmar_exclusao.html", {"horario": horario})
