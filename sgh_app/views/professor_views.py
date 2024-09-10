from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from sgh_app.models.centro import Centro
from sgh_app.models.coordenacao import Coordenacao
from sgh_app.models.curso import Curso
from sgh_app.models.professor import Professor
from sgh_app.forms import ProfessorForm

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sgh_app.models.coordenacao import Coordenacao
from sgh_app.models.professor import Professor
from sgh_app.models.centro import Centro
from sgh_app.forms import ProfessorForm

@login_required
def listar_professores(request):
    try:
        # Obtém a coordenação associada ao usuário logado
        coordenacao = request.user.coordenacao
        curso = coordenacao.curso  # Curso associado ao usuário logado

        # Filtra os professores com base no curso da coordenação
        professores = Professor.objects.filter(curso=curso)
        centros = Centro.objects.all()  # Para escolher o centro

        if request.method == 'POST':
            form = ProfessorForm(request.POST)
            if form.is_valid():
                professor = form.save(commit=False)
                professor.curso = curso  # Define o curso com base no usuário logado
                professor.save()
                messages.success(request, 'Professor cadastrado com sucesso!')
                return redirect('listar_professores')
        else:
            form = ProfessorForm()

        context = {
            'professores': professores,
            'form': form,
            'centros': centros  # Lista de centros para escolha
        }

        return render(request, 'professor.html', context)

    except Coordenacao.DoesNotExist:
        messages.error(request, 'Você não está associado a uma coordenação de curso.')
        return redirect('logout')
    

