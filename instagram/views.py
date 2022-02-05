from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from usuarios.views import seguidores
from .models import Postagem, Comentario, Mensagem
from usuarios.models import Perfil



def index(request):
    if request.user.is_authenticated:
        postagens = Postagem.objects.order_by('data')
        perfil = Perfil.objects.exclude(user=request.user) & Perfil.objects.exclude(seguidores=request.user)[:3]
        contexto = {
            'postagens': postagens,
            'perfils': perfil,
        }
        return render(request,'index.html', contexto)
    return redirect('login')

def perfil(request, pk):
    perfil_usuario = get_object_or_404(Perfil, pk=pk)
    user = perfil_usuario.user
    postagens = Postagem.objects.filter(usuario=user.perfil.pk)
    numero_de_postagem = Postagem.objects.filter(usuario=user.perfil.pk).count()
    seguindo = Perfil.objects.filter(seguidores=user).count()
    contexto = {
        'usuario': user,
        'postagens': postagens,
        'numero_de_postagem': numero_de_postagem,
        'seguindo': seguindo
    }
    return render(request, 'perfil.html', contexto)

def like(request):
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('postid'))
        posts = get_object_or_404(Postagem, id=id)
        if request.user in posts.like.all():
            posts.like.remove(request.user)
            posts.save()
            result = posts.quantidade_de_like()
            resposta = 'remover'
        else:
            posts.like.add(request.user.id)
            posts.save()
            result = posts.quantidade_de_like()
            resposta = 'adicionar'
        
        return JsonResponse({'result': result, 'resposta': resposta })

def comentar(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)
    usuario = get_object_or_404(Perfil, pk= request.user.perfil.pk)
    comentar = request.POST['comentar']
    comentario = Comentario.objects.create(postagem=postagem, comentario=comentar, usuario=usuario)
    comentario.save()
    return redirect('index')

def visualizar_post(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)
    comentarios = Comentario.objects.filter(postagem=pk)
    contexto = {
        'postagem': postagem,
        'comentarios' : comentarios
    }
    return render (request, 'visualizar_post.html', contexto)

def busca(request):
    perfil_buscado = Perfil.objects.all()
    if 'busca' in request.GET:
        busca_perfil = request.GET['busca']
        if busca:
            perfil_buscado = perfil_buscado.filter(nome__icontains=busca_perfil)
    postagem = Postagem.objects.filter(usuario=perfil_buscado[0:1])
    contexto = {
        'perfis': perfil_buscado,
        'postagem': postagem
    }
    return render (request, 'busca.html', contexto)

def mensagem(request):
    mensagem = Mensagem.objects.exclude(emissario=request.user.perfil).distinct('emissario_id').order_by('emissario_id', '-data')
   
    contexto = {
        'mensagens': mensagem       
    }
    return render(request, 'mensagem.html', contexto)

def inbox(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    mensagem_inbox = Mensagem.objects.filter(emissario=perfil, destinatario=request.user.perfil)| Mensagem.objects.filter(emissario=request.user.perfil, destinatario=perfil) 
    mensagem = Mensagem.objects.exclude(emissario=request.user.perfil).distinct('emissario_id').order_by('emissario_id', '-data')
    contexto = {
        'mensagem_inbox': mensagem_inbox,
        'perfil': perfil,
        'mensagens': mensagem
    }
    return render(request, 'inbox.html', contexto)

def postar(request, pk):
    perfil =get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        foto = request.FILES['foto']
        descricao = request.POST['descricao']
        postagem = Postagem.objects.create(usuario= perfil, foto= foto, descricao=descricao )
        postagem.save()
        return redirect('index')
    contexto = {
        'perfil': perfil
    }
    return render(request, 'publicar.html', contexto)
