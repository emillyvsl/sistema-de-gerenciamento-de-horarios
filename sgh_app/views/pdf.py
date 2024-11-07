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
    ano = request.GET.get('ano')
    semestre_id = request.GET.get('semestre')
    dias_semana = DiasSemana.objects.all()
    pesquisa_realizada = False

    horarios = (
        HorariosDisciplinas.objects.filter(horario_curso__curso=curso)
        .select_related('disciplina', 'ano_semestre', 'horario_curso')
        .prefetch_related('horario_curso__dias_semana')
        .order_by("periodo", "horario_curso__hora_inicio")
    )

    if ano and semestre_id:
        horarios = horarios.filter(ano_semestre__ano=ano, ano_semestre__semestre_id=semestre_id)
        pesquisa_realizada = True
    else:
        try:
            ultimo_ano_semestre = AnoSemestre.objects.filter(curso=curso).latest('ano', 'semestre')
            horarios = horarios.filter(ano_semestre=ultimo_ano_semestre)
        except AnoSemestre.DoesNotExist:
            horarios = None

    horarios_unicos = []
    horarios_vistos = set()
    disciplina_colors = {}

    if horarios:
        for horario in horarios:
            chave_horario = (
                horario.horario_curso.hora_inicio,
                horario.horario_curso.hora_fim,
                horario.periodo,
                tuple(dia.nome for dia in horario.horario_curso.dias_semana.all())
            )

            if chave_horario not in horarios_vistos:
                horarios_vistos.add(chave_horario)
                horarios_unicos.append(horario)

                alocacoes = HorariosDisciplinas.objects.filter(
                    horario_curso=horario.horario_curso,
                    ano_semestre=horario.ano_semestre
                )
                horario.alocacoes_list = alocacoes

                for alocacao in alocacoes:
                    if alocacao.disciplina:
                        disciplina = alocacao.disciplina.nome
                        if disciplina not in disciplina_colors:
                            disciplina_colors[disciplina] = "#{:06x}".format(hash(disciplina) & 0xFFFFFF)
                        alocacao.disciplina_cor = disciplina_colors[disciplina]

    colspan_value = len(dias_semana) + 2

    context = {
        'horarios': horarios_unicos,
        'semestres': semestres,
        'dias_semana': dias_semana,
        'colspan_value': colspan_value,
        'pesquisa_realizada': pesquisa_realizada,
    }

    template = get_template('horarios/horarios_disciplinas_pdf.html')
    html_content = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="horarios_disciplina.pdf"'

    HTML(string=html_content).write_pdf(response)

    return response
