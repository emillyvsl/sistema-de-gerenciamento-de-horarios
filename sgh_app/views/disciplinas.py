from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.coordenacao import Coordenacao
from sgh_app.models.disciplina import Disciplina
from sgh_app.models.periodo import Periodo
from sgh_app.forms import DisciplinaForm

@login_required
def listar_disciplinas(request):
    try:
        # Obtém a coordenação associada ao usuário logado
        coordenacao = request.user.coordenacao
        curso = coordenacao.curso  # Curso associado ao usuário logado

        # Filtra as disciplinas com base no curso da coordenação
        disciplinas = Disciplina.objects.filter(curso=curso)

        # Obtém todos os períodos do curso, independente de ter disciplinas associadas
        periodos = Periodo.objects.filter(tipo_periodo__periodos__disciplinas__curso=curso).distinct()

        if request.method == 'POST':
            form = DisciplinaForm(request.POST)
            if form.is_valid():
                disciplina = form.save(commit=False)
                disciplina.curso = curso  # Define o curso com base no usuário logado
                disciplina.save()
                messages.success(request, 'Disciplina cadastrada com sucesso!')
                return redirect('listar_disciplinas')
        else:
            # Filtra os períodos pelo curso do usuário logado
            form = DisciplinaForm()
            form.fields['periodo'].queryset = Periodo.objects.filter(tipo_periodo__periodos__disciplinas__curso=curso).distinct()

        context = {
            'disciplinas': disciplinas,
            'form': form,
            'curso': curso,
        }

        return render(request, 'disciplinas.html', context)

    except Coordenacao.DoesNotExist:
        messages.error(request, 'Você não está associado a uma coordenação de curso.')
        return redirect('logout')

