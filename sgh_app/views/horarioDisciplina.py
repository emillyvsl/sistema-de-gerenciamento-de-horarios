from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.semestre import Semestre  # Certifique-se de que este import está correto

@login_required
def horarioDisciplina(request):
    # Obtendo a coordenação do usuário logado
    coordenacao = request.user.coordenacao

    # Verifica se o usuário logado tem a coordenação associada ao curso
    if not coordenacao:
        messages.error(request, "Acesso negado: você não possui coordenação associada.")
        return redirect('home')  # Redirecione para a página inicial ou onde desejar

    # Obtém o curso associado à coordenação
    curso = coordenacao.curso

    # Filtra os horários de disciplinas pelo curso da coordenação
    horarios_disciplinas = HorariosDisciplinas.objects.select_related(
        'disciplina_professor__disciplina', 
        'disciplina_professor__professor', 
        'horario_curso__curso',
        'ano_semestre'
    ).prefetch_related('horario_curso__dias_semana').filter(
        horario_curso__curso=curso  # Filtra pelos horários do curso
    )

    # Buscando todos os semestres
    semestres = Semestre.objects.all()  # Certifique-se de que o modelo Semestre está correto

    context = {
        'horarios_disciplinas': horarios_disciplinas,
        'semestres': semestres,  # Adicionando a lista de semestres ao contexto
    }
    return render(request, 'horarios/horarios_disciplinas.html', context)
