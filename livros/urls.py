from django.urls import path
from .views import lista_livros, alugar_livro, meus_alugueis, criar_conta, devolver_livro, logout_view

urlpatterns = [
    path('', lista_livros, name='lista_livros'),
    path('alugar/<int:livro_id>/', alugar_livro, name='alugar_livro'),
    path('meus-alugueis/', meus_alugueis, name='meus_alugueis'),
    path('criar-conta/', criar_conta, name='criar_conta'),
    path('devolver/<int:aluguel_id>/', devolver_livro, name='devolver_livro'),
    path('logout/', logout_view, name='logout'),
]
