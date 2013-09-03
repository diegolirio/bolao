__author__ = 'diegolirio'

from django import template
from core.models import *

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
	
