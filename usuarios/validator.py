from django.shortcuts import redirect
from email_validator import validate_email
from password_validator import PasswordValidator
from django.contrib.auth.models import User

from usuarios.models import Perfil



def valida_email(email):
    return validate_email(email)

def valida_nome(nome):
    return nome.isalpha()

def valida_senha(senha,senha2):
    schema = PasswordValidator()
    schema.min(6).has().uppercase().has().lowercase().has().no().spaces()
    return (schema.validate(senha) and senha == senha2)

def nome_unico(nome):
    return User.objects.filter(username=nome).exists()

def nome_unico_perfil(nome):
    return Perfil.objects.filter(nome=nome).exists()
