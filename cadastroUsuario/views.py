import html

from django.db import connection
from django.shortcuts import render

from cadastroUsuario.form import CadastroUsuarioForm
from noticia.models import Noticia


def home(request):  
    ult_noticia = Noticia.objects.all()
    ult_noticia = tratarConteudo(ult_noticia)
    if request.method == 'POST':
        ult_noticia = fetchbuscarTag(request.POST.get('buscar-tag'))
        print('-----------------------------------------------------')
        print(ult_noticia)
        return render(request, 'categorias.html',
                      {
                        'ult_noticias': ult_noticia
                        })
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
    return render(request, 'cadastroUsuario.html', contexto)


def login(request):
    return render(request, 'login.html')


def fetchUltimoRegistro():
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT * FROM noticia_noticia
                    ORDER BY id DESC limit 4;""")
        ult_noticia = cursor.fetchall()
        if ult_noticia:
            columns = [col[0] for col in cursor.description]
            ult_noticias_dicts = [
                dict(zip(columns, noticia)) for noticia in ult_noticia
            ]
        return ult_noticias_dicts


def fetchbuscarTag(buscar_tag):
    ult_noticia = []
    if buscar_tag:
        ult_noticia.extend(Noticia.objects.filter(
            titulo__icontains=buscar_tag
        ))
        ult_noticia.extend(Noticia.objects.filter(
            id_categoria__categoria__icontains=buscar_tag
        ))
        return ult_noticia
    else:
        return Noticia.objects.all()


def tratarConteudo(ult_noticia):
    for noticia in ult_noticia:
        noticia.conteudo = html.unescape(noticia.conteudo)
    return ult_noticia


def categorias(request, categoria):
    noticias = Noticia.objects.filter(
        id_categoria__categoria__icontains=categoria
    )
    print(noticias)
    contexto = {
        'ult_noticias': noticias,
        'categoria': categoria
    }

    return render(request, 'categorias.html', contexto)
