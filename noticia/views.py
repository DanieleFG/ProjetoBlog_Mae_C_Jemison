import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from PIL import Image

from cadastroUsuario.models import Cadastro

from .form import NoticiaForm
from .models import Noticia


def listarNoticias(request):
    noticias = Noticia.objects.all()
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user).first()
        print('usuario User')
        print(user)    
        if user.is_staff:
            noticias = Noticia.objects.all()
        else:
            noticias = Noticia.objects.filter( id_autor__autor__icontains=usuario_dados.nome)
    return render(request, 'noticia/listarNoticias.html',
                  {'noticias': noticias, 'usuarios': usuario_dados})


def adicionarNoticia(request):

    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user).first()
        print('usuario User')
        print(user)
    if request.method == 'POST':
        form = NoticiaForm(request.POST)
        file = request.FILES.get("image")
        img = Image.open(file)
        ext = file.split('.')[-1]
        print(file)
        today = datetime.now().strftime('%Y%m%d%H%M%S')
        new_filename = f'img_{today}.{ext}'
        
        path = os.path.join(settings.BASE_DIR, f'media/uploads/noticia/\
                            {new_filename}')
        img = img.save(path)
        if form.is_valid():
            form.save()
            return redirect('listarNoticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticia/adicionarNoticia.html', 
                  {
                    'form': form,
                    'usuarios': usuario_dados.nome
                    })


class Noticia(LoginRequiredMixin, DetailView):
    template_name = 'noticia.html'
    model = Noticia
    login_url = reverse_lazy('login')


def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('listarNoticias')
    else:
        form = NoticiaForm(instance=noticia)
    return render(
            request,
            'noticia/adicionarNoticia.html',
            {'form': form, 'noticia': pk})
