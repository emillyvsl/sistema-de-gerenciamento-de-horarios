from django.shortcuts import render
from django.db import IntegrityError

from sgh_app.models.ano_semestre import AnoSemestre
from sgh_app.models.horario_curso import HorarioCurso
from sgh_app.models.horarios_disciplinas import HorariosDisciplinas

def gerarHorarios(request):
    if request.method == 'POST':
        # Tente obter o AnoSemestre
        ano_semestre = AnoSemestre.objects.filter(id=1).first()  # Use filter e first para evitar o erro
        if not ano_semestre:
            # Lide com o caso onde o AnoSemestre não existe
            print("AnoSemestre não encontrado.")
            return render(request, 'template.html', {'error': 'AnoSemestre não encontrado.'})

        # Tente obter o HorarioCurso (substitua o ID conforme necessário)
        horario_curso = HorarioCurso.objects.filter(id=1).first()  # Use filter e first aqui também
        if not horario_curso:
            print("HorarioCurso não encontrado.")
            return render(request, 'template.html', {'error': 'HorarioCurso não encontrado.'})

        # Crie o objeto HorariosDisciplinas permitindo disciplina_professor como nulo
        novo_horario = HorariosDisciplinas(
            disciplina_professor=None,
            horario_curso=horario_curso,
            ano_semestre=ano_semestre
        )

        try:
            novo_horario.save()
        except IntegrityError as e:
            print(f'Erro ao salvar: {e}')

    return render(request, 'template.html')
