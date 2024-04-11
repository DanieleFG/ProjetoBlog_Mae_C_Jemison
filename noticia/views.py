import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from PIL import Image

from cadastroUsuario.models import Cadastro

from .form import NoticiaForm
from .models import Noticia


def listarNoticias(request):
    noticias = Noticia.objects.all()
    contexto = {}
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user.email).first()
        contexto = {"usuarios": usuario_dados}
        print("usuario User")
        print(usuario_dados.nome)
        if user.is_staff:
            noticias = Noticia.objects.all()
        else:
            noticias = Noticia.objects.filter(
                id_autor__autor__icontains=usuario_dados.nome
            )

    contexto["noticias"] = noticias
    return render(request, "noticia/listarNoticias.html", contexto)


def adicionarNoticia(request):
    if request.user.is_authenticated:
        user = request.user
        usuario_dados = Cadastro.objects.filter(email=user.email).first()
        print("usuario User")
        print(user)
    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)  # Não salva no banco ainda
            file = request.FILES.get("imagem")
            img = Image.open(file)
            ext = file.name.split(".")[-1]
            today = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"img_{today}.{ext}"
            # settings.MEDIA_ROOT = settings.MEDIA_ROOT.replace("\", '/')
            path = os.path.join(settings.MEDIA_ROOT, "uploads/noticias", filename)
            img.save(path)
            path_image = os.path.join("uploads/noticias", filename)
            if path_image.find("\\") != -1:
                path_image = os.path.join("uploads/noticias", filename).replace("\\", "/")
            noticia.imagem = path_image # Salva o caminho no banco
            noticia.save()  # Agora sim, salva no banco
            return redirect("listarNoticias")
    else:
        form = NoticiaForm()
    return render(
        request,
        "noticia/adicionarNoticia.html",
        {"form": form, "usuarios": usuario_dados},
    )


def excluir_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    noticia.delete()
    return redirect("listarNoticias")


def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    print("_______Editar____________")
    print(noticia)
    if request.method == "POST":
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect("listarNoticias")
    else:
        form = NoticiaForm(instance=noticia)
    return render(
        request, "noticia/adicionarNoticia.html", {"form": form, "noticia": pk}
    )


class NoticiaView(DetailView):
    template_name = "noticia.html"
    model = Noticia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["usuarios"] = Cadastro.objects.filter(
                email=self.request.user.email
            ).first()
            print(context)
        return context
