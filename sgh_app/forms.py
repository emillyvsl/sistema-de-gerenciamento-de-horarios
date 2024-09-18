# forms.py
from django import forms
from sgh_app.models.disciplina import Disciplina
from sgh_app.models.periodo import Periodo
from .models import Professor

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'centro'] 

class DisciplinaForm(forms.ModelForm):
    periodo = forms.ModelChoiceField(queryset=Periodo.objects.all(), empty_label="Selecione o período")

    class Meta:
        model = Disciplina
        fields = ['nome', 'periodo']