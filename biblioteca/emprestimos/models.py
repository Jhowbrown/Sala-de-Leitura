from django.db import models
from django.contrib.auth.models import User  # Usaremos o modelo User embutido no Django
from django.utils import timezone

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    disponivel = models.BooleanField(default=True)
    #quantidade_exemplares = models.IntegerField(default=1)  # Definindo o campo corretamente

    def __str__(self):
        return self.titulo


class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE) # Relacionando com o modelo User
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    devolvido = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.livro.titulo} emprestado para {self.aluno.username}'
    
    

