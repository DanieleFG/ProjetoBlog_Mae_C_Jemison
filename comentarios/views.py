from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ComentarioForm

# Create your views here.


def adicionar_comentario(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('detalhes_postagem')
    else:
        form = ComentarioForm()
    return render(request, 'comentarios/adicionar_comentario.html',
                  {'form': form})
