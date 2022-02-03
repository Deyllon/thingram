from django.contrib import admin
from .models import Postagem, Comentario, Mensagem

admin.site.register(Postagem)
admin.site.register(Comentario)
admin.site.register(Mensagem)

