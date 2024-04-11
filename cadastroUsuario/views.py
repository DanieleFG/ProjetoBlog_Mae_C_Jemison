import html

from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.shortcuts import render, redirect
from noticia.models import Categoria, Noticia


from cadastroUsuario.form import CadastroUsuarioForm
from cadastroUsuario.models import Cadastro


def home(request):
    ult_noticia = Noticia.objects.all()
    ult_noticia = tratarConteudo(ult_noticia)
    noticia_recente = fetchUltimoRegistro()
    contexto = {"ult_noticias": ult_noticia}
    contexto["lancamentos"] = noticia_recente
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user.email).first()
        print("usuario User---------")
        print(usuario_dados.nome)
        contexto["usuarios"] = usuario_dados
    if request.method == "POST":
        ult_noticia = fetchbuscarTag(request.POST.get("buscar-tag"))
        contexto["ult_noticias"] = ult_noticia
        # print('-----------------------------------------------------')
        # print(ult_noticia)
        return render(request, "categorias.html", contexto)

    print(contexto)
    return render(request, "home.html", contexto)


def cadastroUsuario(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    sucesso = False
    form = CadastroUsuarioForm(request.POST or None)
    if form.is_valid():
        sucesso = True
        form.save()

    contexto = {"form": form, "sucesso": sucesso}
    return render(request, "cadastroUsuario.html", contexto)


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "login.html")


def fetchUltimoRegistro():
    categorias_com_noticias = Categoria.objects.annotate(num_noticias=Count("noticia"))
    categorias_com_noticias = categorias_com_noticias.filter(num_noticias__gt=0)
    categorias_aleatorias = categorias_com_noticias.order_by("?")[:3]

    ult_noticias_dict = []

    for categoria in categorias_aleatorias:
        ult_noticia = (
            Noticia.objects.filter(id_categoria=categoria.id).order_by("-id").first()
        )

        if ult_noticia:
            ult_noticias_dict.append(
                {
                    "categoria": ult_noticia.id_categoria,
                    "titulo": ult_noticia.titulo,
                    "imagem": ult_noticia.imagem,
                    "pk": ult_noticia.pk,
                }
            )

    return ult_noticias_dict


def fetchbuscarTag(buscar_tag):
    ult_noticia = []
    if buscar_tag:
        ult_noticia.extend(Noticia.objects.filter(titulo__icontains=buscar_tag))
        ult_noticia.extend(
            Noticia.objects.filter(id_categoria__categoria__icontains=buscar_tag)
        )
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
        print("usuario User")
        print(usuario_dados.nome)
        contexto["usuarios"] = usuario_dados
    noticias = Noticia.objects.filter(id_categoria__categoria__icontains=categoria)
    noticia_recente = fetchUltimoRegistro()
    contexto["ult_noticias"] = noticias
    contexto["categoria"] = categoria
    contexto["lancamentos"] = noticia_recente

    return render(request, "categorias.html", contexto)


def logout_user(request):
    logout(request)
    return redirect("home")


def verificar_cadastro(request):
    ult_noticia = Noticia.objects.all()
    ult_noticia = tratarConteudo(ult_noticia)

    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        noticia_recente = fetchUltimoRegistro()
        usuario = authenticate(request, username=email, password=senha)

        if usuario:
            login(request, usuario)
            user = request.user
            usuario_dados = Cadastro.objects.filter(email=user.email).first()
            return render(
                request,
                "home.html",
                {
                    "usuarios": usuario_dados,
                    "lancamentos": noticia_recente,
                    "ult_noticias": ult_noticia,
                },
            )
        
        elif request.POST.get("buscar-tag"):
            ult_noticia = fetchbuscarTag(request.POST.get("buscar-tag"))
            contexto = {"ult_noticias": ult_noticia}
            return render(request, "categorias.html")
        
        else:
            contexto = {"erro_login": "Usuário não autenticado!"}
            return render(request, "login.html", contexto)
