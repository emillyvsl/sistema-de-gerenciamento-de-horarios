from django.contrib import admin

from sgh_app.models.dias_semana import DiasSemana
from sgh_app.models.horario_curso import HorarioCurso
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

admin.site.register(Centro)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Coordenacao)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Semestre)
admin.site.register(DiasSemana, DiasSemanaAdmin)
admin.site.register(HorarioCurso, HorarioCursoAdmin)
