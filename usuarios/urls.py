from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('seguidores/<int:pk>', views.seguidores, name='seguidores'),
    path('edita_perfil/<int:pk>', views.edita_perfil, name='edita_perfil')
]