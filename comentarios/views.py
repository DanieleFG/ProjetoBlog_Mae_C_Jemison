from django.shortcuts import render, redirect
from django.contrib import messages
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
            return redirect('detalhes_postagem')  # Redirecionar para a página de detalhes da postagem
    else:
        form = ComentarioForm()
    return render(request, 'comentarios/adicionar_comentario.html', {'form': form})
