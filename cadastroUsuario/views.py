from django.shortcuts import render
from cadastroUsuario.form import CadastroUsuarioForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def cadastroUsuario(request):
    sucesso = False
    form = CadastroUsuarioForm(request.POST or None)
    if form.is_valid():
        sucesso = True
        form.save()
    contexto = {
        'form': form,
        'sucesso': sucesso
    }
    return render (request, 'cadastroUsuario.html', contexto)

def login(request):
    return render(request, 'login.html')