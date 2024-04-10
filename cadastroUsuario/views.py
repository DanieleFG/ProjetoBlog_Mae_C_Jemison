import html

from django.contrib.auth import authenticate , login, logout
from django.db.models import Count
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render,  redirect, get_object_or_404

from cadastroUsuario.form import CadastroUsuarioForm
from cadastroUsuario.models import Cadastro
from noticia.models import Categoria, Noticia
from django.contrib.auth.models import User



def home(request):  
    ult_noticia = Noticia.objects.all()
    ult_noticia = tratarConteudo(ult_noticia)
 
    noticia_recente = fetchUltimoRegistro()
    print(noticia_recente)
    contexto = {'ult_noticias': ult_noticia}
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user.email).first()
        print('usuario User---------')
        print(usuario_dados.nome)
        contexto['usuarios'] = usuario_dados
    if request.method == 'POST':
        ult_noticia = fetchbuscarTag(request.POST.get('buscar-tag'))
        contexto['ult_noticias'] = ult_noticia
        # print('-----------------------------------------------------')
        # print(ult_noticia)
        return render(request, 'categorias.html', contexto)

    print(contexto)
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


def loginView(request):   
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
    print('______TAG_________')
    print(buscar_tag)
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
    contexto = {}
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user.email).first()
        print('usuario User')
        print(usuario_dados.nome)
        contexto['usuarios'] = usuario_dados
    noticias = Noticia.objects.filter(
        id_categoria__categoria__icontains=categoria
    )
    # print(noticias)
    contexto['ult_noticias'] = noticias
    contexto['categoria'] = categoria
    # contexto = {
    #     'ult_noticias': noticias,
    #     'categoria': categoria,
    # }
    return render(request, 'categorias.html', contexto)

def logout_user(request):
    logout(request)
    return redirect('home')

def verificar_cadastro(request):
    ult_noticia = Noticia.objects.all()
    ult_noticia = tratarConteudo(ult_noticia)
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = authenticate(request, username=email, password=senha)
        if usuario:
            print('usuario auth')
            print(usuario)
            usuario_dados = Cadastro.objects.filter(email=email).first()
            print('usuario Cad')
            print(usuario_dados.nome)
            # Verifica se existe um usuário com o email fornecido
            if usuario:
                print('Login-------------')
                print(login(request, usuario))
                return render(request, 'home.html', {'usuarios': usuario_dados, 'ult_noticias': ult_noticia})
            else:
                # Usuário não autenticado
                return HttpResponse("Usuário não autenticado!")
        else:
            # Usuário não autenticado
            return HttpResponse("Usuário não autenticado!")
        
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user).first()
        print('usuario User')
        print(user)

    return render(request, 'home.html', {'usuarios': usuario_dados, 'ult_noticias': ult_noticia})