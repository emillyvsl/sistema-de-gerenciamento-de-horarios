# Generated by Django 5.1 on 2024-09-18 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgh_app', '0002_alter_semestre_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='semestre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodos', to='sgh_app.semestre'),
        ),
    ]
