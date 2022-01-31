from django.shortcuts import redirect, render
from .models import Postagem, Comentario
from usuarios.models import Perfil
def index(request):
    if request.user.is_authenticated:
        postagens = Postagem.objects.all()
        perfil = Perfil.objects.exclude(user=request.user)[:3]
        contexto = {
            'postagens': postagens,
            'perfil': perfil
        }
        return render(request,'index.html', contexto)
    return redirect('login')

