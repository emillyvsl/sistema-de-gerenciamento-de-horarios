from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

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
    return render(request, 'auth/login.html')
