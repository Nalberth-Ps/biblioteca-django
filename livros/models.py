from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    quantidade = models.PositiveIntegerField(default=1)
    resumo = models.TextField(blank=True)

    @property
    def disponivel(self):
        return self.quantidade > 0

    def __str__(self):
        return self.titulo

class Aluguel(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_aluguel = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)
    data_devolucao_prevista = models.DateField(default=timezone.now() + timedelta(days=14))
    multa = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    @property
    def calcular_multa(self):
        if self.data_devolucao:
            if self.data_devolucao > self.data_devolucao_prevista:
                dias_atraso = (self.data_devolucao - self.data_devolucao_prevista).days
                return dias_atraso * 1.00  # Por exemplo, 1.00 por dia de atraso
            else:
                return 0.00
        else:
            if timezone.now().date() > self.data_devolucao_prevista:
                dias_atraso = (timezone.now().date() - self.data_devolucao_prevista).days
                return dias_atraso * 1.00  # Por exemplo, 1.00 por dia de atraso
            else:
                return 0.00

    def save(self, *args, **kwargs):
        self.multa = self.calcular_multa
        super(Aluguel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.livro.titulo} alugado por {self.usuario.username}'
