# forms.py
from django import forms
from .models import Professor

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'centro'] 
