from django.db import models
from usuarios.models import Perfil

class Postagem(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos/%d/%m/%Y', blank=False)
    

class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=500)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)