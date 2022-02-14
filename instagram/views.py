
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from usuarios.views import seguidores
from .models import Postagem, Comentario, Mensagem, Notificacao
from usuarios.models import Perfil



def index(request):
    if request.user.is_authenticated:
        postagens = Postagem.objects.order_by('-data')
        perfil = Perfil.objects.exclude(user=request.user) & Perfil.objects.exclude(seguidores=request.user).order_by('seguidores')[:3]
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
            notificacao = Notificacao.objects.create(tipo=1,de=request.user.perfil, para= posts.usuario, postagem=posts)
            notificacao.save()
            
        return JsonResponse({'result': result, 'resposta': resposta })

def comentar(request):
    id = int(request.POST.get('postid'))
    user_id = int(request.POST.get('usuario'))
    comentario_feito = request.POST.get('comentario')
    postagem = get_object_or_404(Postagem, id=id)
    usuario = get_object_or_404(Perfil, id= user_id)
    comentar = comentario_feito
    comentario = Comentario.objects.create(postagem=postagem, comentario=comentar, usuario=usuario)
    comentario.save()
    notificacao = Notificacao.objects.create(postagem=postagem,tipo=2,para=postagem.usuario, de=request.user.perfil,)
    notificacao.save()
    return HttpResponse('Comentario feito com sucesso')

def visualizar_post(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)
    comentarios = Comentario.objects.filter(postagem=pk)
    contexto = {
        'postagem': postagem,
        'comentarios' : comentarios
    }
    return render (request, 'visualizar_post.html', contexto)

def busca(request):
    jsonn = None
    perfil = request.POST.get('perfil')
    perfil_buscado = Perfil.objects.filter(nome__icontains=perfil)
    if len(perfil_buscado) > 0 and len(perfil) > 0:
        data = []
        for perfis in perfil_buscado:
            k = {
                'pk': perfis.pk,
                'nome': perfis.nome,
                'foto': str(perfis.foto.url) 
            }
            data.append(k)
        jsonn = data
    else:
        jsonn = 'Nenhum perfil encontrado'
    return JsonResponse({'data': jsonn})
    
def mensagem(request):
    mensagem = Mensagem.objects.exclude(emissario=request.user.perfil).filter(destinatario = request.user.perfil.pk).distinct('emissario_id').order_by('emissario_id', '-data')
   
    contexto = {
        'mensagens': mensagem       
    }
    return render(request, 'mensagem.html', contexto)

def inbox(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
   
    mensagem = mensagem = Mensagem.objects.exclude(emissario=request.user.perfil).filter(destinatario = request.user.perfil.pk).distinct('emissario_id').order_by('emissario_id', '-data')
    contexto = {
        
        'perfil': perfil,
        'mensagens': mensagem
    }
    return render(request, 'inbox.html', contexto)

def enviar_mensagem(request):
    id_emissario = int(request.POST.get('ide'))
    id_destinatario = int(request.POST.get('idd'))
    emissario = get_object_or_404(Perfil, id=id_emissario)
    destinatario = get_object_or_404(Perfil, id=id_destinatario)
    conteudo = request.POST.get('mensagem_conteudo')
    mensagem = Mensagem.objects.create(conteudo=conteudo, emissario=emissario,destinatario=destinatario, emissario_nome=emissario.nome)
    mensagem.save()
    return HttpResponse('Mensagem feita com sucesso')

def postar(request, pk):
    perfil =get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        if 'foto' in request.FILES:
            foto = request.FILES['foto']
        else:
            return redirect('postar', pk=perfil.id)
        descricao = request.POST['descricao']
        postagem = Postagem.objects.create(usuario= perfil, foto= foto, descricao=descricao )
        postagem.save()
        return redirect('index')
    contexto = {
        'perfil': perfil
    }
    return render(request, 'publicar.html', contexto)

def ler_mensagem(request,pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    mensagem = Mensagem.objects.filter(emissario=perfil, destinatario=request.user.perfil)| Mensagem.objects.filter(emissario=request.user.perfil, destinatario=perfil) 
    return JsonResponse({"messages":list(mensagem.values())})

def notificacao_postagem(request, notificacao_pk, postagem_pk):
    notificacao = Notificacao.objects.get(pk=notificacao_pk)
    notificacao.usuario_viu = True
    notificacao.save()
    return redirect('visualizar_post', postagem_pk)

def notificacao_perfil(request, notificacao_pk, perfil_pk):
    notificacao = Notificacao.objects.get(pk=notificacao_pk)
    notificacao.usuario_viu = True
    notificacao.save()
    return redirect('perfil', perfil_pk )

def deletar(request):
    id = int(request.POST.get('postagem_id'))
    postagem = get_object_or_404(Postagem, id=id)
    postagem.delete()
    return redirect('index')

def deletar_comentario(request):
    id = int(request.POST.get('comentario_id'))
    comentario = get_object_or_404(Comentario,id=id )
    comentario.delete()
    return HttpResponse('Comentario apagado com sucesso')

def ler_comentarios(request,pk):
    id_postagem = int(request.GET.get('postagem_id'))
    postagem = get_object_or_404(Postagem, id=id_postagem)
    comentarios = Comentario.objects.filter(postagem=postagem)
    data = []
    for comentario in comentarios:
        k = {
            'pk': comentario.pk,
            'nome': comentario.usuario.nome,
            'conteudo': comentario.comentario,
            'foto': str(comentario.usuario.foto.url),
            'usuario': comentario.usuario.pk,
            'usuario_atual': request.user.perfil.pk
        }
        data.append(k)
    return JsonResponse({'data': data})