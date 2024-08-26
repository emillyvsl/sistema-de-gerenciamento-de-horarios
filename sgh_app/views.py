from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib import messages
from django.contrib.auth import logout

from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

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

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user.username
        data = timezone.now()
        data = localtime(data)  # Converter para o fuso horário configurado
        messages.success(request, 'Seu formulário foi enviado com sucesso!')


    return render(request, 'index.html', {'user': user, 'data': data})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')