from django.contrib import admin
from .models import Livro, Aluguel, Autor, Categoria

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'quantidade', 'data_publicacao', 'editora')
    search_fields = ('titulo', 'autor__nome', 'isbn')
    list_filter = ('autor', 'categorias', 'editora', 'data_publicacao')
    fieldsets = (
        (None, {
            'fields': ('titulo', 'autor', 'isbn', 'quantidade', 'resumo', 'capa')
        }),
        ('Informações Adicionais', {
            'classes': ('collapse',),
            'fields': ('data_publicacao', 'editora', 'categorias'),
        }),
    )
    filter_horizontal = ('categorias',)

class AluguelAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'data_aluguel', 'data_devolucao_prevista', 'data_devolucao', 'multa', 'status')
    search_fields = ('livro__titulo', 'usuario__username')
    list_filter = ('data_devolucao_prevista', 'data_devolucao', 'status')

admin.site.register(Autor, AutorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Livro, LivroAdmin)
admin.site.register(Aluguel, AluguelAdmin)
