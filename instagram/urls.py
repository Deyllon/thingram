from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/<int:pk>', views.perfil, name='perfil'),
    path('like/', views.like, name='like'),
    path('comentar/<int:pk>', views.comentar, name='comentar'),
    path('post/<int:pk>', views.visualizar_post, name='visualizar_post'),
    path('busca/', views.busca, name='busca'),
    path('mensagem/', views.mensagem, name='mensagem'),
    path('inbox/<int:pk>', views.inbox, name='inbox'),
    path('postar/<int:pk>', views.postar, name='postar')
]