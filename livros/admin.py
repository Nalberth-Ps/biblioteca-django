from django.contrib import admin
from .models import Livro, Aluguel
from unfold.admin import ModelAdmin

class CustomAdminClass(ModelAdmin):
    pass

class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn')
    search_fields = ('titulo', 'autor', 'isbn')
    list_filter = ('titulo', 'autor', 'isbn')
    fieldsets = (
        (None, {
            'fields': ('titulo', 'autor', 'isbn')
        }),
        ('Informações Adicionais', {
            'classes': ('collapse',),
            'fields': ('data_publicacao', 'resumo'),
        }),
    )

class AluguelAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'data_aluguel', 'data_devolucao_prevista', 'data_devolucao', 'multa')
    search_fields = ('livro__titulo', 'usuario__username')
    list_filter = ('data_devolucao_prevista', 'data_devolucao')

admin.site.register(Livro, LivroAdmin)
admin.site.register(Aluguel, AluguelAdmin)