
from django import template
from instagram.models import Notificacao


register = template.Library()

@register.inclusion_tag('partials/notificacao.html', takes_context= True)
def ver_notificacao(context):
    usuario = context['request'].user.perfil
    notificacao = Notificacao.objects.filter(para=usuario).exclude(de=usuario).exclude(usuario_viu=True).order_by('-data')
    notificacao_vista =  Notificacao.objects.filter(para=usuario).exclude(usuario_viu=False).exclude(de=usuario).order_by('-data')
    return {'notificacoes':notificacao,
            'notificacao_vista': notificacao_vista}