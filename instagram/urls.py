from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/<int:pk>', views.perfil, name='perfil'),
    path('like/', views.like, name='like'),
    path('comentar/', views.comentar, name='comentar'),
    path('post/<int:pk>', views.visualizar_post, name='visualizar_post'),
    path('busca/', views.busca, name='busca'),
    path('mensagem/', views.mensagem, name='mensagem'),
    path('inbox/<int:pk>', views.inbox, name='inbox'),
    path('postar/<int:pk>', views.postar, name='postar'),
    path('enviar_mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
    path('ler_mensagem/<int:pk>', views.ler_mensagem, name='ler_mensagem'),
    path('notificacao/<int:notificacao_pk>/post<int:postagem_pk>', views.notificacao_postagem, name='notificacao_postagem'),
    path('notificacao/<int:notificacao_pk>/perfil<int:perfil_pk>', views.notificacao_perfil, name='notificacao_perfil'),
    path('deletar_postagem/', views.deletar, name='deletar'),
    path('deletar_comentario/', views.deletar_comentario, name='deletar_comentario')
]