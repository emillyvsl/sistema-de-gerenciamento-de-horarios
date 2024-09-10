from django.urls import path
from .views.auth_views import login, user_logout, registro
from .views.professor_views import excluir_professor, listar_professores
from .views.index_views import index  # Se você criar um arquivo separado para a view `index`

urlpatterns = [
    path('', login, name='login'), 
    path('registro/', registro, name='registro'),
    path('index/', index, name='index'),
    path('logout/', user_logout, name='logout'),
    path('professores/', listar_professores, name='listar_professores'),
    path('professor/excluir/<int:professor_id>/', excluir_professor, name='excluir_professor'),
   
]