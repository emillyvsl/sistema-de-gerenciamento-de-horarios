from django.contrib import admin

from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas
from sgh_app.models.preferencias import Preferencias
from .models import Centro, Curso, Coordenacao, Periodo, Semestre

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'centro', 'quantidade_periodos')
    search_fields = ('nome',)
    list_filter = ('centro',)

class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'semestre',)  
    search_fields = ('semestre__nome',)  
    list_filter = ('semestre',)  


class DiasSemanaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class HorarioCursoAdmin(admin.ModelAdmin): #deve ser retirado depois
    list_display = ('curso', 'hora_inicio', 'hora_fim')
    search_fields = ('curso__nome',)
    list_filter = ('curso',)


class PreferenciasAdmin(admin.ModelAdmin):
    list_display = ('professor', 'get_dias_preferidos', 'get_horas_preferidas')
    
    def get_dias_preferidos(self, obj):
        return ', '.join([dia.nome for dia in obj.dias_preferidos.all()])
    get_dias_preferidos.short_description = 'Dias Preferidos'
    
    def get_horas_preferidas(self, obj):
        return ', '.join([hora.__str__() for hora in obj.horas_preferidas.all()])
    get_horas_preferidas.short_description = 'Horas Preferidas'


class HorariosDisciplinasAdmin(admin.ModelAdmin):
    list_display = ('get_disciplina', 'get_professor', 'horario_curso', 'ano_semestre')
    search_fields = ('disciplina_professor__disciplina__nome', 'disciplina_professor__professor__nome')
    list_filter = ('horario_curso__curso', 'ano_semestre')

    def get_disciplina(self, obj):
        return obj.disciplina_professor.disciplina.nome
    get_disciplina.short_description = 'Disciplina'

    def get_professor(self, obj):
        return obj.disciplina_professor.professor.nome
    get_professor.short_description = 'Professor'


class AnoSemestreAdmin(admin.ModelAdmin):
    list_display = ('ano', 'semestre')  # Campos que serão exibidos na listagem
    search_fields = ('ano',)  # Campos que podem ser pesquisados
    list_filter = ('semestre',)  # Campos pelos quais é possível filtrar 

admin.site.register(Centro)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Coordenacao)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Semestre)
admin.site.register(DiasSemana, DiasSemanaAdmin)
admin.site.register(HorarioCurso, HorarioCursoAdmin)
admin.site.register(Preferencias, PreferenciasAdmin)
admin.site.register(HorariosDisciplinas, HorariosDisciplinasAdmin)
admin.site.register(AnoSemestre, AnoSemestreAdmin)

