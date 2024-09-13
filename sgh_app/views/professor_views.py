from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from sgh_app.models.centro import Centro
from sgh_app.models.coordenacao import Coordenacao
from sgh_app.models.curso import Curso
from sgh_app.models.disciplina import Disciplina
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
        disciplinas = Disciplina.objects.all()  # Lista de disciplinas
        adicionar_disciplina_url = reverse('adicionar_disciplina_professor')



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
            'centros': centros,  # Lista de centros para escolha
            'curso': curso,
            'disciplinas': disciplinas,  # Lista de disciplinas
            'adicionar_disciplina_url': adicionar_disciplina_url, 
        }

        return render(request, 'professor.html', context)

    except Coordenacao.DoesNotExist:
        messages.error(request, 'Você não está associado a uma coordenação de curso.')
        return redirect('logout')
    


@login_required
def excluir_professor(request, professor_id):
    # Verifica se o método da requisição é POST
    if request.method == 'POST':
        # Tenta obter o objeto Professor com o ID fornecido. Se não encontrar, retorna um erro 404.
        professor = get_object_or_404(Professor, id=professor_id)
        try:
            # Tenta excluir o objeto Professor do banco de dados
            professor.delete()
            # Adiciona uma mensagem de sucesso à sessão
            messages.success(request, 'Professor excluído com sucesso!')
            
            # Verifica se a requisição foi feita via AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Retorna uma resposta JSON indicando sucesso
                return JsonResponse({'success': True})
            
            # Redireciona para a página de listagem de professores
            return redirect('listar_professores')
        except Exception as e:
            # Se houver um erro ao tentar excluir o professor
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Retorna uma resposta JSON indicando falha e a mensagem de erro
                return JsonResponse({'success': False, 'error': str(e)})
            
            # Redireciona para a página de listagem de professores
            return redirect('listar_professores')
    else:
        # Se o método da requisição não for POST
        messages.error(request, 'Método inválido.')
        # Redireciona para a página de listagem de professores
        return redirect('listar_professores')
    
@login_required
def editar_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)

    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            # Adiciona uma mensagem de sucesso à sessão
            messages.success(request, 'Professor(a) editado com sucesso!')
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Retorna uma resposta JSON indicando sucesso
                return JsonResponse({'success': True})
            return redirect('listar_professores')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Retorna uma resposta JSON indicando falha e os erros do formulário
                return JsonResponse({'success': False, 'errors': form.errors})
            return redirect('listar_professores')
    else:
        # Se o método da requisição não for POST
        messages.error(request, 'Método inválido.')
        # Redireciona para a página de listagem de professores
        return redirect('listar_professores')
    
   



