__author__ = 'diegolirio'

from django import template
from core.models import *
from core.const import *

register = template.Library()

@register.filter('hello')
def hello(obj):
    return  'Ola ' + obj
	
@register.filter('cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')	

@register.filter('get_patrocinador_principal_display')	
def get_patrocinador_principal_display(competicao):
	try:
		patrocinador = Competicao_Patrocinadores.objects.filter(competicao=competicao, principal=True)[0:1].get()
	except:
		return ''	
	return patrocinador.patrocinador.nome_visual
	
@register.filter('get_patrocinador_principal_link')	
def get_patrocinador_principal_link(competicao):
	try:
		patrocinador = Competicao_Patrocinadores.objects.filter(competicao=competicao, principal=True)[0:1].get()
	except:
		return ''
	return patrocinador.patrocinador.url_site	
	
@register.filter('get_patrocinador_principal_img')	
def get_patrocinador_principal_img(competicao):
	try:
		patrocinador = Competicao_Patrocinadores.objects.filter(competicao=competicao, principal=True)[0:1].get()
	except:
		return ''
	return patrocinador.patrocinador.image_aside	

@register.filter('get_comentarios_atividade')	
def get_comentarios_atividade(atividade):
	return ComentarioAtividade.objects.filter(atividade=atividade)
	
@register.filter('get_qtde_comentarios')	
def get_qtde_comentarios(atividade):
	return ComentarioAtividade.objects.filter(atividade=atividade).count()
	
@register.filter('get_aproveitamento')		
def get_aproveitamento(inscricao):
	grupos = Grupo.objects.filter(campeonato=inscricao.competicao.campeonato)
	qtde = 0
	for g in grupos:
		jgs_aux = Jogo.objects.filter(grupo=g)
		for j in jgs_aux:
			if j.status.codigo != 'E':
				qtde = qtde + 1
	if qtde > 0:
		pontuacao_100_ = PONTOS_PLACAR * qtde
		aproveitamento = inscricao.pontos * 100 / pontuacao_100_ 
	else:
		aproveitamento = 100
	return aproveitamento
	
	
	
	
	
	
	
	
	
	
	
