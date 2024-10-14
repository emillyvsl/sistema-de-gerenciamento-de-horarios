from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
import os

from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.semestre import Semestre

def gerar_pdf(request):
    # Obter os mesmos dados que você passa para a view original
    coordenacao = request.user.coordenacao
    curso = coordenacao.curso if coordenacao else None
    semestres = Semestre.objects.all()

    ano = request.GET.get('ano')
    semestre_id = request.GET.get('semestre')

    dias_semana = DiasSemana.objects.all()
    pesquisa_realizada = False
    horarios = None

    # Obter os horários
    if curso:
        horarios = HorariosDisciplinas.objects.filter(horario_curso__curso=curso).select_related(
            'disciplina_professor__disciplina',
            'disciplina_professor__professor',
            'ano_semestre',
            'horario_curso'
        ).prefetch_related('horario_curso__dias_semana')

        if ano and semestre_id:
            horarios = horarios.filter(ano_semestre__ano=ano, ano_semestre__semestre_id=semestre_id)
            pesquisa_realizada = True
        else:
            try:
                ultimo_ano_semestre = AnoSemestre.objects.latest('ano', 'semestre')
                horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
            except AnoSemestre.DoesNotExist:
                horarios = None

    # Preparar o contexto do template
    context = {
        'horarios': horarios,
        'semestres': semestres,
        'pesquisa_realizada': pesquisa_realizada,
        'dias_semana': dias_semana,
    }

    # Carregar o novo template HTML com os dados
    template = get_template('horarios/horarios_disciplinas_pdf.html')  # Certifique-se de usar o template correto
    html_content = template.render(context)

    # Gerar o PDF usando WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="horarios_disciplina.pdf"'

    # Converter HTML para PDF
    HTML(string=html_content).write_pdf(response)

    return response
