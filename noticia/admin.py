from django.contrib import admin

from noticia.models import Autor, Categoria, Noticia


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_publicacao']
    search_fields = ['titulo', 'data_publicacao']
    list_filter = ['data_publicacao']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['categoria']
    search_fields = ['categoria']
    list_filter = ['categoria']


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['autor', 'descricao', 'status']
    search_fields = ['autor', 'descricao']
    list_filter = ['autor']
