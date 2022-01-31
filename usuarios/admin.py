from django.contrib import admin
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class PerfilAdmin(admin.StackedInline):
    model = Perfil
    can_delete = True
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
