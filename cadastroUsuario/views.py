import html

from django.contrib.auth import authenticate
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from cadastroUsuario.form import CadastroUsuarioForm
from cadastroUsuario.models import Cadastro
from noticia.models import Categoria, Noticia


def home(request):  
    ult_noticia = Noticia.objects.all()
    ult_noticia = tratarConteudo(ult_noticia)
 
    noticia_recente = fetchUltimoRegistro()
    print(noticia_recente)
    if request.method == 'POST':
        ult_noticia = fetchbuscarTag(request.POST.get('buscar-tag'))
        return render(request, 'categorias.html',
                      {
                        'ult_noticias': ult_noticia,
                        'lancamentos': noticia_recente
                        })
    contexto = {
        'ult_noticias': ult_noticia,
        'lancamentos': noticia_recente  
    }
    return render(request, 'home.html', contexto)


def cadastroUsuario(request):

    form = CadastroUsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()

    contexto = {
        'form': form,
    }
    return render(request, 'login.html', contexto)


def loginView(request):
    return render(request, 'login.html')


def fetchUltimoRegistro():

    categorias_com_noticias = Categoria.objects.annotate(num_noticias=Count('noticia'))
    categorias_com_noticias = categorias_com_noticias.filter(num_noticias__gt=0)
    categorias_aleatorias = categorias_com_noticias.order_by('?')[:3]

    ult_noticias_dict = []

    for categoria in categorias_aleatorias:
        ult_noticia = Noticia.objects.filter(id_categoria=categoria.id)\
            .order_by('-id').first()
        
        if ult_noticia:
            ult_noticias_dict.append({
                "categoria": ult_noticia.id_categoria,
                "titulo": ult_noticia.titulo,
                "imagem": ult_noticia.imagem,
                "pk": ult_noticia.pk
            })
            
    return ult_noticias_dict


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
    noticia_recente = fetchUltimoRegistro()
    contexto = {
        'ult_noticias': noticias,
        'categoria': categoria,
        'lancamentos': noticia_recente
    }

    return render(request, 'categorias.html', contexto)


def verificar_cadastro(request):
    ult_noticia = Noticia.objects.all()
    ult_noticia = tratarConteudo(ult_noticia)
    noticia_recente = fetchUltimoRegistro()
    
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = authenticate(request, username=email, password=senha)
        usuario_dados = Cadastro.objects.filter(email=email).first()
    
        if usuario:
            return render(request, 'home.html', {
                'usuarios': usuario_dados.nome,
                'ult_noticias': ult_noticia,
                'lancamentos': noticia_recente}
            )
        else:
            return HttpResponse("Usuário não autenticado!")
        
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user).first()

        

    return render(request, 'home.html', {
        'usuarios': usuario_dados.nome,
        'ult_noticias': ult_noticia,
        'lancamento': noticia_recente}
    )