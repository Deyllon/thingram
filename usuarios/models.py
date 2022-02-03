from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=1000)
    foto = models.ImageField(upload_to='fotos/perfil/%d/%m/%Y', default='usuario-de-perfil.png' ,blank=True, null=True)
    bio = models.TextField(max_length=500, default='')
    seguidores = models.ManyToManyField(User, related_name='seguidores')
    
    def quantidade_de_seguidores(self):
        return self.seguidores.count()
    
@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    instance.perfil.save()
    