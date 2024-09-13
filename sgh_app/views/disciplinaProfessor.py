from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
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
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
