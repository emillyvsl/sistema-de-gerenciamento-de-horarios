from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'), 
    path('registro/', views.registro, name='registro'),
    path('index/', views.index, name='index'),
    path('logout/', views.user_logout, name='logout'),
    path('professores/', views.listar_professores, name='listar_professores'),

]