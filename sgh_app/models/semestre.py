from django.db import models

class Semestre(models.Model):
    NOME_OPCOES = [
        ('primeiro_semestre', '1º semestre letivo'),
        ('segundo_semestre', '2º semestre letivo'),
        ('dple', 'DPLE'),
        
    ]

    nome = models.CharField( max_length=50, choices=NOME_OPCOES)

    def __str__(self):
        return dict(self.NOME_OPCOES).get(self.nome, self.nome)
