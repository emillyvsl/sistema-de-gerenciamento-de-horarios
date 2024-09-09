from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib import messages
from django.contrib.auth import logout

from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

from sgh_app.forms import ProfessorForm
from sgh_app.models.coordenacao import Coordenacao
from sgh_app.models.curso import Curso
from sgh_app.models.professor import Professor



def registro(request):
    if request.method == 'GET':
        return render(request, 'auth/cadastro.html')
    else:
        username = request.POST['nome']
        password = request.POST['senha']
        email = request.POST['email']

        try:
            # Verificar se o usuário já existe
            user = User.objects.get(email=email)
            return HttpResponse("Email já registrado.")
        except User.DoesNotExist:
            # Criar um novo usuário
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                return HttpResponse("Usuário registrado com sucesso!")
            except IntegrityError:
                return HttpResponse("Erro ao registrar o usuário.")
@csrf_protect
def login(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html')
    else:
        email = request.POST['email']
        password = request.POST['senha']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)  # Autentica e loga o usuário
                return redirect('index')   # Redireciona para a view index
            else:
                return HttpResponse("Senha incorreta.")
        except User.DoesNotExist:
            return HttpResponse("Usuário não encontrado.")

@login_required  # Garante que o usuário esteja autenticado para acessar a página
def index(request):
    # Obter a coordenação do usuário logado
    coord = getattr(request.user, 'coordenacao', None) #A função getattr é uma função incorporada em Python que é usada para obter o valor de um atributo de um objeto.
    
    # Verifica se o usuário tem uma coordenação associada
    if coord:
        curso = coord.curso  # Obtém o curso associado à coordenação
        nome_coordenacao = coord.nome
        nome_centro = curso.centro.nome  # Obtém o nome do centro associado ao curso
    
        
        # Contexto a ser enviado ao template
        context = {
            'user': request.user.username,  # Nome de usuário do usuário logado
            'data': localtime(timezone.now()),  # Data e hora atual no fuso horário local
            'curso': curso,  # Curso associado à coordenação
            'centro': nome_centro,  # Nome do centro associado ao curso
            'nome_coordenacao': nome_coordenacao,
         
        }
        # Renderiza o template 'index.html' com o contexto
        return render(request, 'index.html', context)
    else:
        # Se o usuário não estiver associado a uma coordenação, exibe uma mensagem de erro
        messages.error(request, 'Você não está associado a uma coordenação de curso.')
        # Redireciona o usuário para a página de logout ou uma página apropriada
        return redirect('logout')


# Função para realizar o logout do usuário
def user_logout(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        logout(request)  # Realiza o logout
    # Redireciona o usuário para a página de login após o logout
    return redirect('login')



@login_required
def listar_professores(request):
    try:
        # Obtém a coordenação associada ao usuário logado
        coordenacao = request.user.coordenacao
        curso = coordenacao.curso

        # Filtra os professores com base no curso da coordenação
        professores = Professor.objects.filter(curso=curso)
        cursos = Curso.objects.filter(id=curso.id)  # Obtém apenas o curso do usuário logado

        if request.method == 'POST':
            form = ProfessorForm(request.POST)
            if form.is_valid():
                professor = form.save(commit=False)
                professor.curso = curso  # Define o curso do professor como o curso da coordenação
                professor.save()
                messages.success(request, 'Professor cadastrado com sucesso!')
                return redirect('listar_professores')
        else:
            form = ProfessorForm()

        context = {
            'professores': professores,
            'form': form,
            'cursos': cursos
        }

        return render(request, 'professor.html', context)

    except Coordenacao.DoesNotExist:
        messages.error(request, 'Você não está associado a uma coordenação de curso.')
        return redirect('logout')