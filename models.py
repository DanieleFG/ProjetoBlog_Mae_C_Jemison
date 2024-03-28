from django.db import models
from ckeditor.fields import RichTextField

class Noticias(models.Model):
    titulo = models.CharField(max_length=255)
    resumo = RichTextField()
    conteudo = RichTextUploadingField()
    Categoria = models.CharField(max_length=20)
    Autor = models.CharField(max_length=15, on_delete=models.PROTECT)
    Data_publicacao = models.DateField(auto_now_add=True)

    def str(self):
        return f'{self.titulo} [{self.Autor}]'

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-data_publicacao']

class autores(models.Model)
    Status_Choice = (
        ('A', 'Ativo'),
        ('I', 'Inativo'),
    )
    Autor = models.CharField(max_length=255)
    Descricao = models.CharField(max_length=500)
    Data_inicio = models.DateField()
    Status = models.CharField(max_length=10, choices=Status_Choice)

    def str(self):
        return f'{self.Autor} [{self.Status}]'

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['Autor']

class Categorias(models.Model):
    Categoria = models.CharField(max_length=255)

    def str(self):
        return f'{self.Categoria}'

    class Meta:
        verbose_name = 'Cadastro de Categorias'
        verbose_name_plural = 'Cadastro de Categorias'
        ordering = ['categoria']


