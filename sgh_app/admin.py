from django.contrib import admin
from .models import Centro, Curso, Coordenacao, Periodo, TipoPeriodo

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'centro', 'quantidade_periodos')
    search_fields = ('nome',)
    list_filter = ('centro',)

class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo_periodo',)  
    search_fields = ('tipo_periodo__nome',)  
    list_filter = ('tipo_periodo',)  

admin.site.register(Centro)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Coordenacao)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(TipoPeriodo)
