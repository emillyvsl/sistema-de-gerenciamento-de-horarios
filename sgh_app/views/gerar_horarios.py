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

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.semestre import Semestre

@login_required
def gerar_horarios(request):
    semestres = Semestre.objects.all()
    periodo_opcoes = []

    if request.method == 'POST':
        ano = request.POST['ano']
        semestre_id = request.POST['semestre']
        paridade = request.POST['paridade']

        print(f"Ano: {ano}, Semestre ID: {semestre_id}, Paridade: {paridade}")  # Verificar os dados recebidos no POST

        if AnoSemestre.objects.filter(ano=ano, semestre_id=semestre_id).exists():
            messages.warning(request, "Esse ano já foi cadastrado neste semestre.")
            return redirect('gerar_horarios')

        semestre = Semestre.objects.get(id=semestre_id)
        ano_semestre = AnoSemestre.objects.create(ano=ano, semestre=semestre)

        coordenacao = request.user.coordenacao
        if not coordenacao:
            messages.error(request, "Acesso negado: você não possui coordenação associada.")
            return redirect('home')
        curso = coordenacao.curso

        # Gerar opções de período com base na quantidade de períodos
        if hasattr(curso, 'quantidade_periodos'):
            for p in range(1, curso.quantidade_periodos + 1):
                # Filtrar períodos pares ou ímpares, garantindo que 'p' seja sempre um número
                if (paridade == 'par' and p % 2 == 0) or (paridade == 'impar' and p % 2 != 0):
                    periodo_opcoes.append(p)

        print(f"Períodos disponíveis: {periodo_opcoes}")  # Verificar quais períodos estão sendo gerados

        # Gerar horários para todos os horários do curso
        horarios_curso = HorarioCurso.objects.filter(curso=curso)

        for horario_curso in horarios_curso:
            for periodo in periodo_opcoes:
                # Criar horários com o período como número
                print(f"Criando horário para o período: {periodo}")  # Verificar o período antes de criar
                HorariosDisciplinas.objects.create(
                    horario_curso=horario_curso,
                    ano_semestre=ano_semestre,
                    disciplina_professor=None,  # Pode ser nulo inicialmente
                    periodo=periodo  # Salvando o número do período aqui
                )

        messages.success(request, 'Ano e semestre cadastrados com sucesso!')
        return redirect('horarios_disciplinas')

    return render(request, 'horarios/gerar_horarios.html', {
        'semestres': semestres,
        'periodo_opcoes': periodo_opcoes,
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
