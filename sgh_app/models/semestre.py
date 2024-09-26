from django.db import models

class Semestre(models.Model):
    # Define uma lista de opções para o campo 'nome'.
    NOME_OPCOES = [
        # Tupla com o valor armazenado no banco e o texto exibido para o usuário.
        ('primeiro_semestre', '1º semestre letivo'),
        ('segundo_semestre', '2º semestre letivo'),
        ('dple', 'DPLE'),
    ]

    # Define o campo 'nome' como um CharField com uma lista de opções restritas.
    nome = models.CharField(max_length=50, choices=NOME_OPCOES)

    def __str__(self):
        # Retorna a representação legível do semestre.
        # Converte a lista de opções em um dicionário para obter o texto correspondente ao valor armazenado.
        # Se o valor armazenado não estiver nas opções, retorna o valor bruto.
        return dict(self.NOME_OPCOES).get(self.nome, self.nome)