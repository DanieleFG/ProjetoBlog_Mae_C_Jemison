from django.shortcuts import redirect, render , get_object_or_404
from django.views.generic import DetailView

from .form import NoticiaForm
from .models import Noticia
from cadastroUsuario.models import Cadastro

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from PIL import Image
import os
from django.conf import settings
from datetime import datetime




def listarNoticias(request):
    noticias = Noticia.objects.all()
    # print(noticias)
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user.email).first()
        print('usuario User')
        print(usuario_dados.nome)
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
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)  # Não salva no banco ainda
            file = request.FILES.get("imagem")
            img = Image.open(file)
            ext = file.name.split('.')[-1]
            today = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f'img_{today}.{ext}'
            path = os.path.join(settings.MEDIA_ROOT, 'uploads/noticias', filename)
            img.save(path)
            noticia.imagem = os.path.join('uploads/noticias', filename)  # Salva o caminho no banco
            noticia.save()  # Agora sim, salva no banco
            return redirect('listarNoticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticia/adicionarNoticia.html', {'form': form, 'usuarios': usuario_dados.nome})

def excluir_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    noticia.delete()
    return redirect('listarNoticias')

def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    print('_______Editar____________')
    print(noticia)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('listarNoticias')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'noticia/adicionarNoticia.html', {'form': form, 'noticia': pk})

class NoticiaView(LoginRequiredMixin,DetailView):
    template_name = 'noticia.html'
    model = Noticia
    login_url = reverse_lazy('login')  # Redireciona para a página de login
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['usuarios'] = Cadastro.objects.filter(email=self.request.user).first()
        return context

