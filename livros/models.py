from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Autor(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    quantidade = models.PositiveIntegerField(default=1)
    resumo = models.TextField(blank=True)
    categorias = models.ManyToManyField(Categoria, blank=True)
    data_publicacao = models.DateField(null=True, blank=True)
    editora = models.CharField(max_length=200, blank=True)
    capa = models.ImageField(upload_to='images/', null=True, blank=True)

    @property
    def disponivel(self):
        return self.quantidade > 0

    def __str__(self):
        return self.titulo

class Aluguel(models.Model):
    TAXA_MULTA_DIARIA = 1.00

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('devolvido', 'Devolvido'),
        ('atrasado', 'Atrasado'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_aluguel = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)
    data_devolucao_prevista = models.DateField(default=timezone.now() + timedelta(days=14))
    multa = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')

    def calcular_multa(self):
        if self.data_devolucao:
            if self.data_devolucao > self.data_devolucao_prevista:
                dias_atraso = (self.data_devolucao - self.data_devolucao_prevista).days
                return dias_atraso * self.TAXA_MULTA_DIARIA
            else:
                return 0.00
        else:
            if timezone.now().date() > self.data_devolucao_prevista:
                dias_atraso = (timezone.now().date() - self.data_devolucao_prevista).days
                return dias_atraso * self.TAXA_MULTA_DIARIA
            else:
                return 0.00

    def save(self, *args, **kwargs):
        self.multa = self.calcular_multa()
        if not self.data_devolucao and timezone.now().date() > self.data_devolucao_prevista:
            self.status = 'atrasado'
        elif self.data_devolucao:
            self.status = 'devolvido'
        super(Aluguel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.livro.titulo} alugado por {self.usuario.username}'
