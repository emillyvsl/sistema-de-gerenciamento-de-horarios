from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sgh_app.models.coordenacao import Coordenacao
from sgh_app.models.curso import Curso
from sgh_app.models.professor import Professor  # Supondo que exista esse modelo
from sgh_app.models.disciplina import Disciplina  # Supondo que exista esse modelo

@login_required  # Garante que o usuário esteja autenticado para acessar a página
def index(request):
    # Obter a coordenação do usuário logado
    coord = getattr(request.user, 'coordenacao', None)
    
    # Verifica se o usuário tem uma coordenação associada
    if coord:
        curso = coord.curso  # Obtém o curso associado à coordenação
        nome_coordenacao = coord.nome
        nome_centro = curso.centro.nome  # Obtém o nome do centro associado ao curso

        # Contar o número de disciplinas e professores associados ao curso
        total_disciplinas = Disciplina.objects.filter(curso=curso).count()
        total_professores = Professor.objects.filter(curso=curso).count()

        # Contexto a ser enviado ao template
        context = {
            'user': request.user.username,  # Nome de usuário do usuário logado
            'data': localtime(timezone.now()),  # Data e hora atual no fuso horário local
            'curso': curso,  # Curso associado à coordenação
            'centro': nome_centro,  # Nome do centro associado ao curso
            'nome_coordenacao': nome_coordenacao,
            'total_disciplinas': total_disciplinas,  # Adiciona a contagem de disciplinas ao contexto
            'total_professores': total_professores,  # Adiciona a contagem de professores ao contexto
        }
        # Renderiza o template 'index.html' com o contexto
        return render(request, 'index.html', context)
    else:
        # Se o usuário não estiver associado a uma coordenação, exibe uma mensagem de erro
        messages.error(request, 'Você não está associado a uma coordenação de curso.')
        # Redireciona o usuário para a página de logout ou uma página apropriada
        return redirect('logout')
