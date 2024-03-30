from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Autor(models.Model):
    status_Choice = (
        ('A', 'Ativo'),
        ('I', 'Inativo'),
    )
    autor = models.CharField(max_length=255)
    descricao = models.CharField(max_length=500)
    data_inicio = models.DateField()
    status = models.CharField(max_length=10, choices=status_Choice)

    def __str__(self):
        return f'{self.autor} [{self.status}]'

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['autor']

class Categoria(models.Model):
    categoria = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.categoria}'

    class Meta:
        verbose_name = 'Cadastro de Categorias'
        verbose_name_plural = 'Cadastro de Categorias'
        ordering = ['categoria']




class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = CKEditor5Field('Text', config_name='extends')
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.pk}, titulo: {self.titulo}, Data: {self.data_publicacao},  texto: {self.conteudo}"
    
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-data_publicacao']