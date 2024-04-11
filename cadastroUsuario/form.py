from django import forms

from cadastroUsuario.models import Cadastro


class CadastroUsuarioForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Cadastro
        fields = [
            "nome",
            "sobrenome",
            "genero",
            "usuario",
            "email",
            "senha",
            "data_nascimento",
        ]
