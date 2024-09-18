from django.db import models

class TipoPeriodo(models.Model):
    NOME_OPCOES = [
        ('impar', '1º semestre letivo'),
        ('par', '2º semestre letivo'),
        ('dple', 'DPLE'),
        ('oferta_especial', 'Oferta Especial')
    ]

    nome = models.CharField(max_length=50, choices=NOME_OPCOES)

    def __str__(self):
        return dict(self.NOME_OPCOES).get(self.nome, self.nome)
