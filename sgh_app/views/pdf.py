from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.semestre import Semestre

def gerar_pdf(request):
    coordenacao = request.user.coordenacao

    if not coordenacao:
        return redirect('index')

    curso = coordenacao.curso
    semestres = Semestre.objects.all()

    # Capturar os parâmetros 'ano' e 'semestre' da URL, enviados na pesquisa
    ano = request.GET.get('ano')
    semestre_id = request.GET.get('semestre')

    dias_semana = DiasSemana.objects.all()
    pesquisa_realizada = False

    # Obter os horários com a relação para os dias da semana, filtrando pelo curso atual
    horarios = HorariosDisciplinas.objects.filter(
        horario_curso__curso=curso  # Filtro pelo curso atual
    ).select_related(
        'disciplina_professor__disciplina',
        'disciplina_professor__professor',
        'ano_semestre',
        'horario_curso'
    ).prefetch_related('horario_curso__dias_semana')

    if ano and semestre_id:
        # Filtrar também por ano e semestre fornecidos pelo usuário
        horarios = horarios.filter(ano_semestre__ano=ano, ano_semestre__semestre_id=semestre_id)
        pesquisa_realizada = True
    else:
        try:
            # Se o ano e semestre não forem fornecidos, buscar o mais recente
            ultimo_ano_semestre = AnoSemestre.objects.filter(curso=curso).latest('ano', 'semestre')
            horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
        except AnoSemestre.DoesNotExist:
            horarios = None

    # Adicionar alocações ao contexto e evitar duplicação de horários
    horarios_unicos = []
    horarios_vistos = set()

    if horarios:
        for horario in horarios:
            # Criar uma "chave" que represente as informações essenciais para evitar duplicação
            chave_horario = (
                horario.horario_curso.hora_inicio,
                horario.horario_curso.hora_fim,
                horario.periodo,
                tuple(dia.nome for dia in horario.horario_curso.dias_semana.all())
            )

            # Se essa chave não foi vista antes, adicionar o horário aos horários únicos
            if chave_horario not in horarios_vistos:
                horarios_vistos.add(chave_horario)
                horarios_unicos.append(horario)

                # Obter todas as alocações para o HorarioCurso, **filtrando pelo ano_semestre correto**
                alocacoes = HorariosDisciplinas.objects.filter(
                    horario_curso=horario.horario_curso,
                    ano_semestre=horario.ano_semestre  # Filtrar pela relação correta de ano_semestre
                )
                horario.alocacoes_list = alocacoes  # Passa todas as alocações desse horário

    colspan_value = len(dias_semana) + 2

    # Preparar o contexto do template
    context = {
        'horarios': horarios_unicos,
        'semestres': semestres,
        'dias_semana': dias_semana,
        'colspan_value': colspan_value,
        'pesquisa_realizada': pesquisa_realizada,
    }

    # Renderizar o template HTML para o PDF
    template = get_template('horarios/horarios_disciplinas_pdf.html')
    html_content = template.render(context)

    # Gerar o PDF usando WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="horarios_disciplina.pdf"'

    # Converter HTML para PDF
    HTML(string=html_content).write_pdf(response)

    return response
