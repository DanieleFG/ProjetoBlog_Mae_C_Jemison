from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.files.storage import default_storage
import os

def upload_to(instance, filename):
    # Obtém a extensão do arquivo
    ext = filename.split('.')[-1]
    # Gera um novo nome para o arquivo
    new_filename = f'uploads/noticias/{instance.pk}.{ext}'
    # Retorna o caminho completo para salvar o arquivo
    return new_filename
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
    imagem = models.ImageField(upload_to=upload_to, blank=True, null=True)
    def save(self, *args, **kwargs):
        # Verifica se o conteúdo tem uma imagem
        if '<img src="' in self.conteudo:
            # Obtém o caminho da imagem no conteúdo
            start = self.conteudo.find('<img src="') + len('<img src="')
            end = self.conteudo.find('"', start)
            img_path = self.conteudo[start:end]
            # Copia a imagem para o novo local
            with default_storage.open(img_path, 'rb') as f:
                self.imagem.save(os.path.basename(img_path), f)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.pk}, titulo: {self.titulo}, Data: {self.data_publicacao},  texto: {self.conteudo}"
    
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-data_publicacao']