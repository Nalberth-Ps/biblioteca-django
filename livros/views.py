from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro, Aluguel
from .forms import LivroForm
from django.shortcuts import render, redirect
from .forms import RegistroForm

def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, 'livros/lista_livros.html', {'livros': livros})

@login_required
def alugar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if livro.disponivel:
        Aluguel.objects.create(usuario=request.user, livro=livro)
        livro.disponivel = False
        livro.save()
        return redirect('lista_livros')
    return render(request, 'livros/detalhe_livro.html', {'livro': livro})

@login_required
def adicionar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.disponivel = True
            livro.save()
            return redirect('lista_livros')
    else:
        form = LivroForm()
    return render(request, 'livros/adicionar_livro.html', {'form': form})

@login_required
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('lista_livros')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livros/editar_livro.html', {'form': form, 'livro': livro})

@login_required
def deletar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if request.method == 'POST':
        livro.delete()
        return redirect('lista_livros')
    return render(request, 'livros/confirmar_delecao.html', {'livro': livro})

@login_required
def lista_alugueis(request):
    alugueis = Aluguel.objects.filter(usuario=request.user)
    return render(request, 'livros/lista_alugueis.html', {'alugueis': alugueis})

@login_required
def devolver_livro(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id=aluguel_id)
    if request.method == 'POST':
        aluguel.data_devolucao = timezone.now()
        aluguel.livro.disponivel = True
        aluguel.livro.save()
        aluguel.save()
        return redirect('lista_alugueis')
    return render(request, 'livros/confirmar_devolucao.html', {'aluguel': aluguel})

def registro(request):
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
    return render(request, 'livros/registro.html', {'form': form})