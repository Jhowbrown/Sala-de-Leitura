# Generated by Django 5.1.2 on 2024-10-18 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emprestimos', '0004_remove_livro_data_publicacao_remove_livro_isbn_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livro',
            name='quantidade_exemplares',
        ),
    ]