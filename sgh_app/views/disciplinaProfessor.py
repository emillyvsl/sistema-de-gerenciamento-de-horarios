from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages  # Importa para usar mensagens
from sgh_app.models.disciplina import Disciplina
from sgh_app.models.disciplina_professor import DisciplinaProfessor
from sgh_app.models.professor import Professor

def adicionar_disciplina_professor(request):
    if request.method == 'POST':
        disciplina_id = request.POST.get('disciplina')
        professor_id = request.POST.get('professor_id')
        
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        professor = get_object_or_404(Professor, id=professor_id)
        
        # Adiciona a disciplina ao professor
        DisciplinaProfessor.objects.create(disciplina=disciplina, professor=professor)
        
        # Adiciona uma mensagem de sucesso
        messages.success(request, 'Disciplina adicionada com sucesso!')
        
        # Redireciona para a lista de professores
        return redirect('listar_professores')
    
    # Se não for um POST, redireciona de volta
    return redirect('listar_professores')

def remover_disciplina_professor(request, disciplina_id):
    disciplina_professor = get_object_or_404(DisciplinaProfessor, id=disciplina_id)
    professor_id = disciplina_professor.professor.id
    disciplina_professor.delete()
    messages.success(request, 'Disciplina removida com sucesso!')
    return redirect('detalhes_professor', professor_id=professor_id)