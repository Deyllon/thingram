from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth



def cadastro(request):
    if request.method == 'POST':
        email = request.POST['email']
        nome = request.POST['nome']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']
        usuario = User.objects.creat(username=nome, email=email, password=senha)
        usuario.save()
        usuario.perfil.nome = nome
        usuario.save()
        usuario_login = auth.authenticate(request, username=nome, password=senha)
        auth.login(request, usuario_login)
        return redirect('index')
    return render(request,'cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha'] 
        usuario_login = auth.authenticate(request, username=email, password=senha)
        auth.login(request, usuario_login)
        return redirect('index')
    return render (request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')