from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro, Aluguel
from .forms import LivroForm, RegistroForm
from django.db import transaction
from datetime import timedelta
from django.contrib import messages

def criar_conta(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('lista_livros')
    else:
        form = RegistroForm()
    return render(request, 'livros/criar_conta.html', {'form': form})

def lista_livros(request):
    livros = Livro.objects.all()
    pendencias = False
    if request.user.is_authenticated:
        alugueis_pendentes = Aluguel.objects.filter(usuario=request.user, multa__gt=0, data_devolucao__isnull=False)
        pendencias = alugueis_pendentes.exists()
        if pendencias:
            messages.error(request, 'Você não pode alugar um livro enquanto tiver multas pendentes. Por favor, regularize sua situação.')

    return render(request, 'livros/lista_livros.html', {'livros': livros, 'pendencias': pendencias})

@login_required
def alugar_livro(request, livro_id):
    alugueis_pendentes = Aluguel.objects.filter(usuario=request.user, multa__gt=0, data_devolucao__isnull=False)
    if alugueis_pendentes.exists():
        messages.error(request, 'Você não pode alugar um livro enquanto tiver multas pendentes. Por favor, regularize sua situação.')
        return redirect('lista_livros')

    livro = get_object_or_404(Livro, id=livro_id)
    if not livro.disponivel:
        messages.error(request, 'Este livro não está disponível no momento.')
        return redirect('lista_livros')

    with transaction.atomic():
        livro.quantidade -= 1
        livro.save()
        data_devolucao_prevista = timezone.now().date() + timedelta(days=14)
        Aluguel.objects.create(livro=livro, usuario=request.user, data_devolucao_prevista=data_devolucao_prevista)

    return redirect('meus_alugueis')

@login_required
def devolver_livro(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id=aluguel_id, usuario=request.user)
    with transaction.atomic():
        aluguel.data_devolucao = timezone.now().date()
        aluguel.save()
        aluguel.livro.quantidade += 1
        aluguel.livro.save()

    return redirect('meus_alugueis')

@login_required
def meus_alugueis(request):
    alugueis = Aluguel.objects.filter(usuario=request.user)
    return render(request, 'livros/meus_alugueis.html', {'alugueis': alugueis})

def logout_view(request):
    auth_logout(request)
    return redirect('lista_livros')
