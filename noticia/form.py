from django import forms
from noticia.models import Noticia, Categoria, Autor
from django_ckeditor_5.widgets import CKEditor5Widget

class NoticiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["conteudo"].required = False
    class Meta:
        model = Noticia
        fields = ['titulo', 'conteudo']
        widgets = {
            "conteudo": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }

class CategotiaForm(forms.ModelForm):
     class Meta:
            model = Categoria
            fields = ['categoria']

class AutorForm(forms.ModelForm):
        class Meta:
              model = Autor
              fields = ['autor', 'descricao', 'data_inicio', 'status']
