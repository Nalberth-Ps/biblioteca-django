# Generated by Django 5.0.7 on 2024-07-16 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0002_livro_data_publicacao_livro_resumo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluguel',
            name='data_aluguel',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='aluguel',
            name='data_devolucao',
            field=models.DateField(blank=True, null=True),
        ),
    ]
