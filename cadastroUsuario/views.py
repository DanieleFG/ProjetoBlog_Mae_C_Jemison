from django.shortcuts import render
from cadastroUsuario.form import CadastroUsuarioForm
from noticia.models import Noticia

# Create your views here.

def home(request):
    # ult_noticia = fetchUltimoRegistro()
    # print(ult_noticia)
    ult_noticia = Noticia.objects.all()
    contexto = {
        'ult_noticias': ult_noticia
    }
    return render(request, 'home.html', contexto)

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

def fetchUltimoRegistro():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT * FROM noticia_noticia ORDER BY id DESC limit 4;""")
        ult_noticia = cursor.fetchall()
        if ult_noticia:
            columns = [col[0] for col in cursor.description]
            ult_noticias_dicts = [dict(zip(columns, noticia)) for noticia in ult_noticia]
        return ult_noticias_dicts
    return None

