from django.shortcuts import redirect, render
from django.views.generic import DetailView

from .form import NoticiaForm
from .models import Noticia


def listarNoticias(request):
    noticias = Noticia.objects.all()
    return render(request, 'noticia/listarNoticias.html',
                  {'noticias': noticias})


def adicionarNoticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listarNoticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticia/adicionarNoticia.html', {'form': form})


class Noticia(DetailView):
    template_name = 'noticia.html'
    model = Noticia
