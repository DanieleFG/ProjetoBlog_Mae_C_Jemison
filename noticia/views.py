from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Noticia
from .form import NoticiaForm

def listarNoticias(request):
    noticias = Noticia.objects.all()
    return render(request, 'noticia/listarNoticias.html', {'noticias': noticias})

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



