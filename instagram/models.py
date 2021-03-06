from datetime import datetime
from django.db import models
from usuarios.models import Perfil
from django.contrib.auth.models import User
from datetime import datetime

class Postagem(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos/%d/%m/%Y', blank=False)
    descricao = models.TextField(max_length=500, default="")
    like = models.ManyToManyField(User, blank=True)
    data = models.DateTimeField(default=datetime.now(), blank=True)
    
    def quantidade_de_like(self):
        return self.like.count()
class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=500)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)   
class Mensagem(models.Model):
    conteudo = models.TextField(max_length=1000)
    data = models.DateTimeField(default=datetime.now, blank=True)
    emissario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='emisario')
    destinatario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='destinatario')
    emissario_nome = models.CharField(max_length=500, default="")

class Notificacao(models.Model):
    #1 = like, 2 = comentario, 3= follow
    tipo = models.IntegerField()
    para = models.ForeignKey(Perfil, related_name='para', on_delete=models.CASCADE, null=True)
    de = models.ForeignKey(Perfil,related_name='de', on_delete=models.CASCADE, null=True)
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE, related_name='postagem', blank=True, null=True)
    data = models.DateTimeField(default=datetime.now())
    usuario_viu = models.BooleanField(default=False)
