from sqlite3 import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from sgh_app.models.coordenacao import Coordenacao
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout



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

@login_required
def user_logout(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        logout(request)  # Realiza o logout
    # Redireciona o usuário para a página de login após o logout
    return redirect('login')
