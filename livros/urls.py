from django.urls import path
from .views import lista_livros, alugar_livro, adicionar_livro, editar_livro, deletar_livro, lista_alugueis, devolver_livro, registro

urlpatterns = [
    path('', lista_livros, name='lista_livros'),
    path('alugar/<int:livro_id>/', alugar_livro, name='alugar_livro'),
    path('adicionar/', adicionar_livro, name='adicionar_livro'),
    path('editar/<int:livro_id>/', editar_livro, name='editar_livro'),
    path('deletar/<int:livro_id>/', deletar_livro, name='deletar_livro'),
    path('alugueis/', lista_alugueis, name='lista_alugueis'),
    path('devolver/<int:aluguel_id>/', devolver_livro, name='devolver_livro'),
    path('registro/', registro, name='registro'),
]
