from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sgh_app.models.coordenacao import Coordenacao
from sgh_app.models.disciplina import Disciplina
from sgh_app.models.periodo import Periodo
from sgh_app.forms import DisciplinaForm

@login_required
def listar_disciplinas(request):
    try:
        coordenacao = request.user.coordenacao
        curso = coordenacao.curso  # Curso associado ao usuário logado

        # Filtra as disciplinas com base no curso da coordenação
        disciplinas = Disciplina.objects.filter(curso=curso)

        # Obtém todos os períodos disponíveis
        periodos = Periodo.objects.all()

        if request.method == 'POST':
            form = DisciplinaForm(request.POST)
            if form.is_valid():
                disciplina = form.save(commit=False)
                disciplina.curso = curso  # Define o curso com base no usuário logado
                disciplina.save()
                messages.success(request, 'Disciplina cadastrada com sucesso!')
                return redirect('listar_disciplinas')
        else:
            form = DisciplinaForm()

        context = {
            'disciplinas': disciplinas,
            'form': form,
            'curso': curso,
            'periodos': periodos,  # Passa os períodos para o template
        }

        return render(request, 'disciplinas.html', context)

    except Coordenacao.DoesNotExist:
        messages.error(request, 'Você não está associado a uma coordenação de curso.')
        return redirect('logout')

    

@login_required
def editar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    periodos = Periodo.objects.all()  # Obtém todos os períodos para preencher o select

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina editada com sucesso!')

            # Verifica se é uma requisição AJAX (JSON)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('listar_disciplinas')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            messages.error(request, 'Erro ao editar disciplina.')
    else:
        form = DisciplinaForm(instance=disciplina)

    return render(request, 'editar_disciplina.html', {
        'form': form,
        'disciplina': disciplina,
        'periodos': periodos  # Envia os períodos para o template
    })


@login_required
def excluir_disciplina(request, disciplina_id):
    # Verifica se o método da requisição é POST
    if request.method == 'POST':
        # Tenta obter o objeto Disciplina com o ID fornecido. Se não encontrar, retorna um erro 404.
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        try:
            # Tenta excluir o objeto Disciplina do banco de dados
            disciplina.delete()
            # Adiciona uma mensagem de sucesso à sessão
            messages.success(request, 'Disciplina excluída com sucesso!')
            
            # Verifica se a requisição foi feita via AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Retorna uma resposta JSON indicando sucesso
                return JsonResponse({'success': True})
            
            # Redireciona para a página de listagem de disciplinas
            return redirect('listar_disciplinas')
        except Exception as e:
            # Se houver um erro ao tentar excluir a disciplina
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Retorna uma resposta JSON indicando falha e a mensagem de erro
                return JsonResponse({'success': False, 'error': str(e)})
            
            # Redireciona para a página de listagem de disciplinas
            return redirect('listar_disciplinas')
    else:
        # Se o método da requisição não for POST
        messages.error(request, 'Método inválido.')
        # Redireciona para a página de listagem de disciplinas
        return redirect('listar_disciplinas')