from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from noticia.models import Autor, Categoria, Noticia


class NoticiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["conteudo"].required = False

    class Meta:
        model = Noticia
        fields = ['titulo', 'conteudo', 'imagem', 'id_autor', 'id_categoria']
        widgets = {
            'conteudo': CKEditor5Widget(config_name='extends')
        }


class CategotiaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['categoria']


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['autor', 'descricao', 'data_inicio', 'status', 'imagem']
