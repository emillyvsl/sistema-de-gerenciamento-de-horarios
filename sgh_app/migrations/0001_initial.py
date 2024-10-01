# Generated by Django 5.1 on 2024-10-01 00:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DiasSemana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(default=1, verbose_name='Periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('primeiro_semestre', '1º semestre letivo'), ('segundo_semestre', '2º semestre letivo'), ('dple', 'DPLE')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('quantidade_periodos', models.PositiveIntegerField()),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgh_app.centro')),
            ],
        ),
        migrations.CreateModel(
            name='Coordenacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coordenacao', to=settings.AUTH_USER_MODEL)),
                ('curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coordenacao', to='sgh_app.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplinas', to='sgh_app.curso')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplinas', to='sgh_app.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='sgh_app.curso')),
                ('dias_semana', models.ManyToManyField(related_name='horarios', to='sgh_app.diassemana')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professores', to='sgh_app.centro')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professores', to='sgh_app.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Preferencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dias_preferidos', models.ManyToManyField(related_name='preferidos', to='sgh_app.diassemana')),
                ('horas_preferidas', models.ManyToManyField(related_name='preferidas', to='sgh_app.horariocurso')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferencias', to='sgh_app.professor')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaProfessor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplina_professores', to='sgh_app.disciplina')),
                ('professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disciplina_professores', to='sgh_app.professor')),
            ],
        ),
        migrations.AddField(
            model_name='periodo',
            name='semestre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodos', to='sgh_app.semestre'),
        ),
        migrations.CreateModel(
            name='AnoSemestre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField()),
                ('semestre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ano_semestres', to='sgh_app.semestre')),
            ],
            options={
                'unique_together': {('ano', 'semestre')},
            },
        ),
        migrations.CreateModel(
            name='HorariosDisciplinas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_semestre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios_disciplinas', to='sgh_app.anosemestre')),
                ('disciplina_professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='horarios_disciplinas', to='sgh_app.disciplinaprofessor')),
                ('horario_curso', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='horarios_disciplinas', to='sgh_app.horariocurso')),
            ],
            options={
                'unique_together': {('disciplina_professor', 'horario_curso', 'ano_semestre')},
            },
        ),
    ]
