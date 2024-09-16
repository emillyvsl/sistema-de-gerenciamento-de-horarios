from django.urls import path

from sgh_app.views.detalhesProfessor import detalhes_professor
from sgh_app.views.disciplinaProfessor import adicionar_disciplina_professor, remover_disciplina_professor
from sgh_app.views.disciplinas import editar_disciplina, excluir_disciplina, listar_disciplinas
from .views.auth_views import login, user_logout, registro
from .views.professor_views import editar_professor, excluir_professor, listar_professores
from .views.index_views import index  # Se você criar um arquivo separado para a view `index`

urlpatterns = [
    path('', login, name='login'), 
    path('registro/', registro, name='registro'),
    path('index/', index, name='index'),
    path('logout/', user_logout, name='logout'),
    path('professores/', listar_professores, name='listar_professores'),
    path('professor/excluir/<int:professor_id>/', excluir_professor, name='excluir_professor'),
    path('professor/editar/<int:professor_id>/', editar_professor, name='editar_professor'),
    path('disciplinas/', listar_disciplinas, name='listar_disciplinas'), 
    path('disciplina/editar/<int:disciplina_id>/', editar_disciplina, name='editar_disciplina'),
    path('disciplina/excluir/<int:disciplina_id>/', excluir_disciplina, name='excluir_disciplina'),  
    path('professores/adicionar-disciplina/', adicionar_disciplina_professor, name='adicionar_disciplina_professor'),
    path('professor/detalhes/<int:professor_id>/', detalhes_professor, name='detalhes_professor'), 
    path('professor/remover_disciplina/<int:disciplina_id>/', remover_disciplina_professor, name='remover_disciplina_professor'),

     ] 
