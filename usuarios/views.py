from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from usuarios.validator import valida_nome
from .validator import nome_unico, valida_email, valida_nome, valida_senha, nome_unico_perfil
from .models import Perfil
from instagram.models import Notificacao



def cadastro(request):
    if request.method == 'POST':
        email = request.POST['email']
        if not valida_email(email):
            return redirect('cadastro')
        nome = request.POST['nome']
        if not valida_nome(nome):
            return redirect('cadastro') 
        if nome_unico(nome):
            return redirect('cadastro')         
        senha = request.POST['senha']
        senha2 = request.POST['senha2']
        if not valida_senha(senha, senha2):
            return redirect('cadastro')
        foto = request.FILES['foto']
        usuario = User.objects.create_user(username=nome, email=email, password=senha)
        usuario.save()
        usuario.perfil.nome = nome
        usuario.perfil.foto = foto
        usuario.save()
        return redirect('login')
    return render(request,'cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha'] 
        nome = User.objects.filter(email=email).values_list('username', flat=True).get()
        usuario_login = auth.authenticate(request, username=nome, password=senha)
        if usuario_login is not None:
            auth.login(request, usuario_login)
            return redirect('index')
    return render (request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def seguidores(request, pk):
    perfil = get_object_or_404(Perfil, id=pk)
    if request.user in perfil.seguidores.all():
        perfil.seguidores.remove(request.user)
    else:
        perfil.seguidores.add(request.user)
        notificacao = Notificacao.objects.create(tipo=3,de=request.user.perfil, para=perfil)
        notificacao.save()
    return redirect('index')

def edita_perfil(request,pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        nome_perfil = request.POST['nome_perfil']
        if nome_unico_perfil(nome_perfil):
            return redirect('edita_perfil', pk) 
        if not nome_perfil:
            nome_perfil= perfil.nome
        
        bio = request.POST['bio']
        if not bio:
            bio=perfil.bio
        
        if 'foto_perfil' in request.FILES:
            foto_perfil = request.FILES['foto_perfil']
            perfil.foto = foto_perfil
        perfil.nome= nome_perfil   
        perfil.bio = bio
        perfil.save()
        return redirect('index')
    contexto = {
        'perfil': perfil
    }
    return render(request, 'editar_perfil.html', contexto)
        
