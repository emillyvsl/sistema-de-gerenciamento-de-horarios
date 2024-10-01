# gerar_horario.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.semestre import Semestre

@login_required
def gerenciar_horarios(request):
    # Listando todos os anos e semestres cadastrados
    anos_semestres = AnoSemestre.objects.all()
    return render(request, 'gerenciar_horarios.html', {
        'anos_semestres': anos_semestres
    })

@login_required
def gerar_horarios(request):
    semestres = Semestre.objects.all()  # Obtenha todos os semestres do banco de dados
    if request.method == 'POST':
        ano = request.POST['ano']
        semestre_id = request.POST['semestre']

        # Verifica se o ano e semestre já foram cadastrados
        if AnoSemestre.objects.filter(ano=ano, semestre_id=semestre_id).exists():
            messages.error(request, 'Esse ano já foi cadastrado neste semestre.')
            return redirect('gerar_horarios')  # Redireciona de volta ao formulário

        # Cadastrando o novo ano e semestre
        semestre = Semestre.objects.get(id=semestre_id)
        ano_semestre = AnoSemestre.objects.create(ano=ano, semestre=semestre)

        # Gerar horários para todos os cursos disponíveis
        cursos = HorarioCurso.objects.filter(curso__isnull=False).distinct()  # Aqui, filtramos os cursos

        for curso in cursos:
            # Criando um horário de disciplinas padrão
            HorariosDisciplinas.objects.create(
                horario_curso=curso,
                ano_semestre=ano_semestre,
                disciplina_professor=None  # A disciplina_professor pode ser nula inicialmente
            )

        messages.success(request, 'Ano e semestre cadastrados com sucesso!')
        return redirect('quadro_horarios', ano_semestre_id=ano_semestre.id)

    return render(request, 'horarios/gerar_horarios.html', {
        'semestres': semestres,  # Adiciona a lista de semestres ao contexto
    })




@login_required
def quadro_horarios(request, ano_semestre_id):
    ano_semestre = get_object_or_404(AnoSemestre, id=ano_semestre_id)
    # Filtrando os horários de disciplinas com prefetch_related para dias_semana
    horarios = HorariosDisciplinas.objects.filter(ano_semestre=ano_semestre).select_related(
        'disciplina_professor__disciplina', 
        'disciplina_professor__professor'
    ).prefetch_related('horario_curso__dias_semana')  # Usando prefetch_related

    return render(request, 'horarios/horarios_disciplinas.html', {
        'horarios': horarios,
    })
