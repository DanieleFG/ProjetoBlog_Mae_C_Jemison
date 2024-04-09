"""
URL configuration for projeto_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from cadastroUsuario.views import cadastroUsuario, categorias, home, loginView, verificar_cadastro
from comentarios.views import adicionar_comentario
from noticia.views import Noticia, adicionarNoticia, listarNoticias

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path(
        'adicionar_comentario/',
        adicionar_comentario,
        name='adicionar_comentario'
    ),
    path("cadastro", cadastroUsuario),
    path("login", loginView),
    path('listarNoticias', listarNoticias, name='listarNoticias'),
    path('adicionarNoticia/', adicionarNoticia, name='adicionarNoticia'),
    path('listarNoticias/<int:pk>', Noticia.as_view(), name='noticia'),
    path('categoria/<str:categoria>', categorias),
    path('logado/', verificar_cadastro, name='logado'),
]

urlpatterns += [
    path("ckeditor5/",
         include('django_ckeditor_5.urls'),
         name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
