# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core import serializers
from core.const import *
from core.models import *
from core.forms import *
import random
import os
#import json
from django.core.mail import send_mail
#import datetime
from django.contrib.auth import authenticate, login

envia_email = False
# Const
ROOT_PROJECT = os.path.dirname(__file__)
SITE_ROOT_ = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = 'http://mybolao.herokuapp.com/'
NOME_BOLAO = 'Super Bolão' # Super Bolão | Super Placar | Pilantras.com | 

def user_login_is_valid(user_request, user_inscricao):
	if user_request.pk == user_inscricao.pk:
		return True
	return False
	
def get_participante_by_user(user, verifica_confirm_email=True):
	user_participante = Participante()
	if user.is_authenticated():
		try:
			user_participante = Participante.objects.filter(user=user)[0:1].get()
			#if (verifica_confirm_email) and (not user_participante.confirm_email):
			#	return redirect('/cadastre_se/')
		except:
			return redirect('/cadastre_se/')
	return user_participante		

def __get_patrocinador_principal__(competicao):
	try:
		patrocinador = Competicao_Patrocinadores.objects.filter(competicao=competicao, principal=True)[0:1].get()
	except:
		patrocinador = Competicao_Patrocinadores()
	return patrocinador
	
def home(request):
	competicoes = Competicao.objects.all()	
	user_participante = get_participante_by_user(request.user)
	my_count = Competicao.objects.filter(presidente=user_participante).count()
	return render_to_response('_base.html',{	'template': 'index.html',
												'titulo': NOME_BOLAO,
												'subtitulo': '',
												'user_participante': user_participante,
												'my_count': my_count,
												'competicoes': competicoes
											})
											
def get_rancking_by_competicao(competicao):
	if competicao.campeonato.status.codigo == 'E' or competicao.valor_aposta == 0:
		inscr = Inscricao.objects.filter(competicao=competicao, ativo=True).order_by('colocacao')
	else:
		if competicao.visivel_participantes_pendente_pagamento:
			inscr = Inscricao.objects.filter(competicao=competicao).exclude(ativo=False).order_by('colocacao')
		else:
			inscr = Inscricao.objects.filter(competicao=competicao, pagamento=True).exclude(ativo=False).order_by('colocacao')
	return inscr
	
def get_inscricao(competicao, participante):
	try:
		user_inscricao = Inscricao.objects.filter(competicao=competicao, participante=participante)[0:1].get()
	except:
		user_inscricao = Inscricao()	
	return user_inscricao
	
def get_patrocinador_pagina(codigo_pagina, competicao):
	patrocinadores_pagina = []
	try:
		pagina = Pagina.objects.filter(codigo_pagina=codigo_pagina)[0:1].get()
		pag_patr = PaginaPatrocinio.objects.filter(pagina=pagina)	
		for pp in pag_patr:
			if pp.competicacao_patrocinador.competicao == competicao:
				patrocinadores_pagina.append(pp)
	except:
		patrocinadores_pagina = []
	return patrocinadores_pagina	
	
def __get_nome_oficial_competicao__(competicao):
	from core.templatetags.functions import *
	return 'Copa ' + get_patrocinador_principal_display(competicao) + ' ' + competicao.nome

def rancking(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	patrocinador = __get_patrocinador_principal__(competicao)
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	inscricoes_competicao = get_rancking_by_competicao(competicao)
	valor_acumulado = inscricoes_competicao.count() * competicao.valor_aposta
	patrocinadores = get_patrocinador_pagina('R', competicao)
	return render_to_response('_base.html', 
							  {     'template': 'rancking.html', 
							        'titulo': 'Rancking', 
							        'subtitulo': __get_nome_oficial_competicao__(competicao),
							        'user_participante': user_participante,
							        'user_inscricao': user_inscricao,
							        'competicao': competicao,
									'patrocinador': patrocinador,
							        #-----------------------------------
							        'valor_acumulado': valor_acumulado,
							        'inscricoes_competicao': inscricoes_competicao,
									'patrocinadores': patrocinadores
							        })
									
def blog(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	atividades = Atividade.objects.filter(competicao=competicao).order_by('data_hora')[0:15]
	return render_to_response('_base.html', 
							  {     'template': 'blog.html', 
							        'titulo': 'Blog', 
							        'subtitulo': 'Feeds ' + __get_nome_oficial_competicao__(competicao),
							        'user_participante': user_participante,
							        'competicao': competicao,
									'user_inscricao': user_inscricao,
									'atividades': atividades
							        })
									
def __get_one_puclicidade_global__(pagina_codigo):
	try:
		pagina = Pagina.objects.filter(codigo_pagina=pagina_codigo)[0:1].get()
		pag_patr = PaginaPatrocinio.objects.get(pagina=pagina)
		patrocinador = pag_patr.competicacao_patrocinador.patrocinador
	except:
		patrocinador = Patrocinador()
	return patrocinador
	
def __get_one_puclicidade_pagina__(pagina_codigo, competicao):
	patrocinador = Patrocinador()
	try:
		pagina = Pagina.objects.filter(codigo_pagina=pagina_codigo)[0:1].get()
		pag_patrs = PaginaPatrocinio.objects.filter(pagina=pagina)
		for pp in pag_patrs:
			if pp.competicacao_patrocinador.competicao == competicao:
				patrocinador = pp.competicacao_patrocinador.patrocinador
				break
	except:
		patrocinador = Patrocinador()
	return patrocinador	

def get_one_puclicidade_pagina(request, pagina_codigo, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)
	patrocinador = __get_one_puclicidade_pagina__(pagina_codigo, competicao)
	try:
		image = patrocinador.image_aside.url
		if patrocinador.pk > 0:
			return_proc = 'N'
		else:
			return_proc = 'W'
	except:
		image = ""
		return_proc = 'W'
	json = {
			 'patrocinador_id': patrocinador.pk,
			 'patrocinador_display': patrocinador.nome_visual,
			 'patrocinador_link': patrocinador.url_site,
			 'patrocinador_image_aside': image,
			 'return_proc': return_proc
		  }    
	dictFields = { 'fields': json }
	to_json = list()
	to_json.append(dictFields)
	return HttpResponse(simplejson.dumps(to_json), mimetype="text/javascript")  	
	                                
def imprimir_rancking(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)
	inscricoes_competicao = get_rancking_by_competicao(competicao)
	return render_to_response('_base_simple.html', 
							  {     'template': 'rancking_table.html', 
							        'inscricoes_competicao': inscricoes_competicao
							        })			
									
def get_jogos_of_the_campeonato(campeonato):
	grupos = Grupo.objects.filter(campeonato=campeonato)
	jgs = []
	for g in grupos:
		js = Jogo.objects.filter(grupo=g).order_by('data_hora')
		gr = ''
		for j in js:
			if gr != j.grupo.descricao:
				j.first_group = True
			gr = j.grupo.descricao
			jgs.append(j)
	return jgs			                                

def tabela(request, competicao_pk):	
	competicao = Competicao.objects.get(pk=competicao_pk)	
	patrocinador = __get_patrocinador_principal__(competicao)
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	jgs = get_jogos_of_the_campeonato(competicao.campeonato)
	patrocinadores = get_patrocinador_pagina('T', competicao)
	return render_to_response('_base.html', 
							  {       'template': 'tabela.html', 
								      'titulo': 'Tabela',
								      'subtitulo': __get_nome_oficial_competicao__(competicao),
								      'user_participante': user_participante,
								      'user_inscricao': user_inscricao,
								      'competicao': competicao,
									  'patrocinador': patrocinador,
								      #----
									  'jogos': jgs,
									  'patrocinadores': patrocinadores
							 })

def get_palpites_all_participantes(jogo, competicao):
	apostas = Aposta.objects.filter(jogo=jogo).order_by('-pontos')
	if competicao.campeonato.status.codigo == 'E' or competicao.valor_aposta == 0:
		inscricoes = Inscricao.objects.filter(competicao=competicao, ativo=True)	
	else:
		if competicao.visivel_participantes_pendente_pagamento:
			inscricoes = Inscricao.objects.filter(competicao=competicao).exclude(ativo=False)
		else:
			inscricoes = Inscricao.objects.filter(competicao=competicao, pagamento=True).exclude(ativo=False)	
	apostas_jogos_competicao = []	
	for a in apostas:
		for i in inscricoes:
			if a.inscricao.pk == i.pk:
				apostas_jogos_competicao.append(a)		
	return apostas_jogos_competicao

# apostas de um soh jogo e competicao Ex: Brasil X Italia (Copa do Mundo 2014 - Della Volpe)
def apostas_jogo(request, competicao_pk, jogo_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	patrocinador = __get_patrocinador_principal__(competicao)
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	jogo = Jogo.objects.get(pk=jogo_pk)
	if (jogo.status.codigo == 'E'):
		return redirect('/tabela/'+str(competicao.pk)+'/')		
	apostas_jogos_competicao = get_palpites_all_participantes(jogo, competicao)
	patrocinadores = get_patrocinador_pagina('A', competicao)
	return render_to_response('_base.html', 
	                          {   'template': 'apostas_jogo.html', 
								  'titulo': 'Palpites de Todos',
								  'subtitulo': __get_nome_oficial_competicao__(competicao),
								  'user_participante': user_participante,
								  'user_inscricao': user_inscricao,
								  'competicao': competicao,	
								  'patrocinador': patrocinador,								  
	                              'jogo': jogo, 
	                              'apostas': apostas_jogos_competicao,
								  'patrocinadores': patrocinadores
	                           })	
	                           
@login_required
def aposta(request, competicao_pk):	
	competicao = Competicao.objects.get(pk=competicao_pk)	
	patrocinador = __get_patrocinador_principal__(competicao)
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)			
	apts = Aposta.objects.filter(inscricao=user_inscricao).order_by('jogo')
	return render_to_response('_base.html', 
	                          {   'template': 'aposta.html', 
								  'subtitulo': __get_nome_oficial_competicao__(competicao),
	                              'titulo': 'Minhas Apostas',
	                              'user_participante': user_participante,
	                              'user_inscricao': user_inscricao,
	                              'competicao': competicao,
								  'patrocinador': patrocinador,		
	                              'apostas': apts, 
								  'total_pontos': user_inscricao.pontos,
	                              'user_inscricao': user_inscricao
	                          })

# Altera aposta, usuario alterando sua propria aposta		
@login_required
def aposta_edit(request, user_aposta_pk):
	execute_transation = 'N'
	model = Aposta.objects.get(pk=user_aposta_pk)
	mensagem = ''	
	form = ApostaForm()
	pagina_patro = get_patrocinador_pagina('E', model.inscricao.competicao)
		
	if len(pagina_patro) > 0:
		publicidade = pagina_patro[0].competicacao_patrocinador.patrocinador.image_aside
	else:
		publicidade = 'images/patrocinadores/anuncie.gif'
	# ToDo...: if model.jogo.data_hora > DateTime.now-4horas: ToDo..:
	if model.jogo.status.codigo == 'E':		
		if request.method == 'POST':
			form = ApostaForm(request.POST, request.FILES, instance=model)
			if form.is_valid():
				model_update = form.save(commit=False)
				if model_update.resultado_a > model_update.resultado_b:
					model_update.vencedor = 'A'
				elif model_update.resultado_a < model_update.resultado_b:
					model_update.vencedor = 'B'
				else:
					model_update.vencedor = 'E'
				model.colocacao = 0
				model.pontuacao = 0
				model.calculado = False
				model_update.save()
				execute_transation = 'S'
				mensagem = 'Aposta alterada com sucesso'
		else:
			form = ApostaForm(instance=model)
			if not model.inscricao.participante.confirm_email:
				mensagem = u'Confirme seu cadastro em seu email para realizar a alteração dos palpites do jogo!'
				execute_transation = 'S'				
	else:
		mensagem = 'Nao sera mais possivel alterar aposta. Jogo encontra-se em ' + model.jogo.status.descricao
		execute_transation = 'S'
	return render_to_response('_base_simple.html', 
	                          {    'template': 'aposta_edit.html', 
	                               'execute_transation': execute_transation,
	                               'aposta': model, 
	                               'form': form, 
								   'publicidade': publicidade,
	                               'mensagem': mensagem}, 
	                          context_instance=RequestContext(request))	      

def __get_jogos_not_edition_by_campeonato__(campeonato):
	jogos_ = list()
	grupos = Grupo.objects.filter(campeonato=campeonato)
	status = StatusJogo.objects.filter(codigo='E')[0:1].get()
	for g in grupos:
		jgs = Jogo.objects.filter(grupo=g).exclude(status=status).order_by('data_hora')
		for j in jgs:
			jogos_.append(j)
	return jogos_			

def perfil_competicao_modal(request, view_inscricao_pk):   
	view_inscricao = Inscricao.objects.get(pk=view_inscricao_pk)
	to_json = list()
	
	view_apostas = list()
	apts_aux = Aposta.objects.filter(inscricao=view_inscricao)
	jogo_ = 0
	for a in apts_aux:
		if (a.jogo.status.codigo == 'A') or (a.jogo.status.codigo == 'F'):
			view_apostas.append(a)	
			jogo_ = jogo_ + 1		
	view_inscricao_json = {
                             'inscricao_id': view_inscricao.id,
							 'participante_id': view_inscricao.participante.id,
							 'participante_apelido': view_inscricao.participante.apelido,
							 'participante_foto': view_inscricao.participante.foto.url,
							 'inscricao_colocacao': view_inscricao.colocacao,
							 'inscricao_pontos': view_inscricao.pontos, 
							 'inscricao_quantidade_acerto_placar': view_inscricao.quantidade_acerto_placar, 
							 'inscricao_quantidade_acerto_vencedor_um_resultado_correto': view_inscricao.quantidade_acerto_vencedor_um_resultado_correto, 
							 'inscricao_quantidade_acerto_vencedor': view_inscricao.quantidade_acerto_vencedor, 
							 'inscricao_quantidade_acerto_empate_erro_placar': view_inscricao.quantidade_acerto_empate_erro_placar,
							 'inscricao_quantidade_acerto_somente_resultado_um_time': view_inscricao.quantidade_acerto_somente_resultado_um_time,
							 'inscricao_quantidade_erro': view_inscricao.quantidade_erro,
							 'quantidade_jogos': jogo_
						  }    
	dictFields = { 'fields': view_inscricao_json }
	to_json.append(dictFields)
	return HttpResponse(simplejson.dumps(to_json), mimetype="text/javascript")  

def get_apostas_pos_edicao(inscricao):
	apostas = list()
	apts_aux = Aposta.objects.filter(inscricao=inscricao).order_by('jogo') # este encarrega de colocar os jogos no grafico (ordernar todos)		
	for a in apts_aux:
		if (a.jogo.status.codigo == 'A') or (a.jogo.status.codigo == 'F'):
			apostas.append(a)		
	return apostas	

def perfil_competicao(request, competicao_pk, view_inscricao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	patrocinador = __get_patrocinador_principal__(competicao)
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	view_inscricao = Inscricao.objects.get(pk=view_inscricao_pk)
	view_apostas = get_apostas_pos_edicao(view_inscricao)
	jogo_ = len(view_apostas)
	return render_to_response('_base.html', 
						      {  
								'template': 'perfil_competicao.html',
								'titulo': view_inscricao.participante.apelido,
								'subtitulo': get_nome_oficial_competicao(competicao), #view_inscricao.competicao.campeonato.nome + ' ' + view_inscricao.competicao.nome,
								'user_participante': user_participante,
								'user_inscricao': user_inscricao,
								'competicao': competicao, 	
								'patrocinador': patrocinador,										
								'view_inscricao': view_inscricao,
								'apostas': view_apostas, # apostas do participante, nao alterar chave por manter mesmo da apostas.html
								'total_pontos': view_inscricao.pontos,
								#'view_apostas_chart': view_apostas_chart,
								'qtde_jogos': jogo_,
								'perfil': True,
								'foto': view_inscricao.participante.foto
							   })
	
def comparar_colocacao(request, competicao_pk, view_inscricao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	view_inscricao = Inscricao.objects.get(pk=view_inscricao_pk)
	view_apostas = get_apostas_pos_edicao(view_inscricao)
	my_apostas = get_apostas_pos_edicao(user_inscricao)
	jogo_ = len(view_apostas)			
	if user_inscricao.pk > 0:
		participantes_inscritos = Inscricao.objects.filter(competicao=competicao).exclude(participante__in=[view_inscricao.participante, user_participante]).order_by('participante')
	else:
		participantes_inscritos = Inscricao.objects.filter(competicao=competicao).exclude(participante=view_inscricao.participante).order_by('participante')
	return render_to_response('_base.html', 
						      {  
								'template': 'comparar_colocacao.html',
								'titulo': u'Histórico de Colocação',
								'subtitulo': view_inscricao.participante.apelido, #view_inscricao.competicao.campeonato.nome + ' ' + view_inscricao.competicao.nome,
								'user_participante': user_participante,
								'user_inscricao': user_inscricao,
								'competicao': competicao, 	
								'view_inscricao': view_inscricao,
								'apostas': view_apostas, # apostas do participante, nao alterar chave por manter mesmo da apostas.html
								'my_apostas': my_apostas,
								'total_pontos': view_inscricao.pontos,
								#'view_apostas_chart': view_apostas_chart,
								'qtde_jogos': jogo_,
								'perfil': True,
								'participantes_inscritos': participantes_inscritos,
								'foto': view_inscricao.participante.foto,
							   })	
							  
#ajax							  
def get_aposta_by_inscricao(request, inscricao_pk):   
	view_inscricao = Inscricao.objects.get(pk=inscricao_pk)	
	apostas = get_apostas_pos_edicao(view_inscricao)			
	retorno = serializers.serialize("json", apostas)
	return HttpResponse(retorno, mimetype="text/javascript")	
	
def get_inscricao_json(request, inscricao_pk):
	view_inscricao = Inscricao.objects.get(pk=inscricao_pk)
	to_json = list()
	view_inscricao_json = {
                             'inscricao_id': view_inscricao.id,
							 'participante_id': view_inscricao.participante.id,
							 'participante_apelido': view_inscricao.participante.apelido,
							 'participante_foto': view_inscricao.participante.foto.url,
							 'inscricao_colocacao': view_inscricao.colocacao,
							 'inscricao_pontos': view_inscricao.pontos, 
							 'inscricao_quantidade_acerto_placar': view_inscricao.quantidade_acerto_placar, 
							 'inscricao_quantidade_acerto_vencedor_um_resultado_correto': view_inscricao.quantidade_acerto_vencedor_um_resultado_correto, 
							 'inscricao_quantidade_acerto_vencedor': view_inscricao.quantidade_acerto_vencedor, 
							 'inscricao_quantidade_acerto_empate_erro_placar': view_inscricao.quantidade_acerto_empate_erro_placar,
							 'inscricao_quantidade_acerto_somente_resultado_um_time': view_inscricao.quantidade_acerto_somente_resultado_um_time,
							 'inscricao_quantidade_erro': view_inscricao.quantidade_erro
							 #'quantidade_jogos': jogo_
						  }    
	dictFields = { 'fields': view_inscricao_json }
	to_json.append(dictFields)
	return HttpResponse(simplejson.dumps(to_json), mimetype="text/javascript")  	
							   
def __get_code_random__():
	code = ''
	for i in range(0,10):
		code = code + str(random.randint(0,9))
		if i > 9:
			break
	return code
	
def __new_participante__(user):
	participante = Participante()
	participante.user = user
	participante.apelido = user.username
	participante.ddd = 11
	#participante.telefone = 
	participante.confirm_send_code = __get_code_random__()
	participante.save()	
	return participante
	
def cadastre_se(request):
	message = ''
	status_transation = 'I'
	user_participante = get_participante_by_user(request.user, False)
	form_user = UserNewForm()
	form_participante = ParticipanteForm()	
	if request.method == 'POST':
		if request.user.is_authenticated():
			status_transation = 'V'
			if 'save_user' in request.POST:
				form_user = UserEditForm(request.POST, request.FILES, instance=request.user)
				form_participante = ParticipanteForm(instance=user_participante)	
				if form_user.is_valid():
					form_user.save()
					message = 'Informações de usuário gravado com sucesso!'
					#return redirect('/cadastre_se/')
			elif 'save_participante' in request.POST:
				form_participante = ParticipanteForm(request.POST, request.FILES, instance=user_participante)
				form_user = UserEditForm(instance=request.user)
				if form_participante.is_valid():	
					form_participante.save()
					message = 'Informações de participante gravado com sucesso!'
					#return redirect('/cadastre_se/')
		else:
			form_user = UserNewForm(request.POST, request.FILES)
			if form_user.is_valid():
				# Validar senhas compativeis.... no link http://www.aprendendodjango.com/funcoes-de-usuarios/
				user = form_user.save()
				#print('save_user >>>>>>>> automatico participante e apos confirm_email ' + user.username)		
				participante = __new_participante__(user)
				emailss = [user.email,]
				send_mail('Conrfimacao de cadastro '+NOME_BOLAO, 'Usuario: '+ user.username +', clique no link para confirmar o cadastro ' + SITE_ROOT + 'confirm_email/'+participante.confirm_send_code+ '/?user='+str(user.pk), 'diegolirio.dl@gmail.com', emailss)
				status_transation = 'V'
				# ToDo...: Realizar Login... aki.....
				#user = authenticate(username=user.username, password=user.password)
				#login(request, user)
				message = 'Cadastro realizado com sucesso, para terminar seu cadastro entre em seu email e faça a confirmação!'
				#return redirect('/cadastre_se/')
	else:
		if request.user.is_authenticated():
			form_user = UserEditForm(instance=request.user)
			if user_participante != None:
				form_participante = ParticipanteForm(instance=user_participante)	
			status_transation = 'V'
	return render_to_response('_base.html', 
	                          {'template': 'cadastre_se.html', 
	                           'titulo': 'Cadastre-se' if not request.user.is_authenticated() else 'Cadastro', 
	                           'subtitulo': '',
	                           'user_participante': user_participante,
	                           'form_user': form_user,
							   'form_participante': form_participante,
							   'status_transation': status_transation,
							   'message': message
	                           }, RequestContext(request))
				
@login_required				
def alterar_senha(request):
	execute_transation = 'N'
	mensagem = ''
	if request.method == 'POST':
		form = UserPasswordForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			execute_transation = 'S'
			mensagem = 'Senha Alterada com sucesso!'
	else:
		form = UserPasswordForm(instance=request.user)
	return render_to_response('_base_simple.html',
	                          { 'template': 'alterar_senha.html', 
	                               'execute_transation': execute_transation,
	                               'user': request.user, 
	                               'form': form, 
	                               'mensagem': mensagem
							}, RequestContext(request))

def photo(request):
	user_participante = get_participante_by_user(request.user)
	mensagem = ''
	execute_transation = 'N'
	if request.method == 'POST':
		form = ParticipanteFotoForm(request.POST, request.FILES, instance=user_participante)
		if form.is_valid():
			form.save()
			execute_transation = 'S'
			mensagem = 'Foto alterada com sucesso!!!'
	else:
		form = ParticipanteFotoForm(instance=user_participante)
	return render_to_response('_base_simple.html', 
	                          {'template': 'photo.html', 
	                           'form': form,
	                           'execute_transation': execute_transation,
	                           'mensagem': mensagem
	                          }, RequestContext(request))
			
"""
def cadastre_se(request):
	status_transation = 'I' # Insert
	user_participante = get_participante_by_user(request.user)
	if request.method == 'POST':
		if request.user.is_authenticated():
			if 'save_user' in request.POST:
				form_user = UserForm(request.POST, request.FILES, instance=request.user)				
				form_participante = ParticipanteForm(instance=user_participante)				
				#print('save_user in request.POST: <<<<<<<<<<<<<<<<<<<<<<< ' + str(form_user['username'].value))
				if form_user.is_valid():
					#print('form_user.is_valid() <<<<<<<<<<<<<<<<<<<<<<< ')
					if form_user['password'].value == form_user['password_confirm'].value:
						#print('form_user.save() <<<<<<<<<<<<<<<<<<<<<<< ')
						form_user.save()
					else:
						return redirect('/home/')
				status_transation = 'V'
			else:
				user_participante = get_participante_by_user(request.user)
				form_participante = ParticipanteForm(request.FILES, request.POST, instance=user_participante)
		else:
			form_user = UserForm(request.FILES, request.POST)
			if form_user.is_valid():
				user = form_user.save()
				participante_new = Participante()
				participante_new.user = user
				participante_new.apelido = user.username
				participante_new.ddd = 11
				#participante_new.telefone = ...
				participante_new.confirm_send_code = '/confirm_email/' + user.username + '/' + __get_code_randow__()
				participante_new.save()
				participante = get_participante_by_user(request.user)
				form_participante = ParticipanteForm(instance=user_participante)
				status_transation = 'V' # Visualizacao
				#user.email()				
				#send_mail('Conrfimacao de cadastro Bolao da Copa', 'http://127.0.0.1:8000'+participante.confirm_send_code, 'diegolirio.dl@gmail.com', [request.user.email])
			else:
				form_participante = ParticipanteForm()
	else:
		form_participante = ParticipanteForm()	
		if request.user.is_authenticated():
			form_user = UserForm(instance=request.user)
			if user_participante != None:
				form_participante = ParticipanteForm(instance=user_participante)
				status_transation = 'A' if not user_participante.confirm_email else 'V' # A=Aguardando | # V=Visualizacao
		else:
			form_user = UserForm()
	return render_to_response('_base.html', 
	                          {'template': 'cadastre_se.html', 
	                           'titulo': 'Cadastre-se' if not request.user.is_authenticated() else 'Cadastro', 
	                           'subtitulo': '',
	                           'user_participante': user_participante,
	                           'form_user': form_user,
							   'form_participante': form_participante,
							   'status_transation': status_transation
	                           }, RequestContext(request))

"""

@login_required
def reenvio_confirm_email(request):
	user_participante = get_participante_by_user(request.user)
	if not user_participante.confirm_email:
		send_mail('Conrfimacao de cadastro '+NOME_BOLAO, 'clique no link para confirmar o cadastro ' +SITE_ROOT+'confirm_email/'+user_participante.confirm_send_code+ '/?user='+str(user_participante.user.pk), 'diegolirio.dl@gmail.com', [user_participante.user.email])
	return redirect('/cadastre_se/')

def confirm_email(request, codigo_confirm):
    #user = User.objects.filter(username=username)[0:1].get()
	user = User.objects.get(pk=request.GET['user'])
	user_participante = get_participante_by_user(request.user)
	if user_participante.confirm_send_code == codigo_confirm:
		if not user_participante.confirm_email:
			user_participante.confirm_email = True
			user_participante.save()		
			return render_to_response('_base.html', {'template': 'confirmado.html', 'titulo': user_participante.apelido, 'subtitulo': 'Confirmado', 'user_participante': user_participante})
	return redirect('/login/')

@login_required
def solicita_inscricao(request, competicao_pk):
	msg = ''
	competicao = Competicao.objects.get(pk=competicao_pk)
	patrocinador = __get_patrocinador_principal__(competicao)
	publicidade = get_patrocinador_pagina('S', competicao)
	if request.user.is_authenticated:
		if competicao.campeonato.status.codigo == 'E':
			user_participante = get_participante_by_user(request.user)
			if user_participante.confirm_email:
				if Inscricao.objects.filter(participante=user_participante, competicao=competicao).count() == 0:
					if Solicitacao.objects.filter(participante=user_participante, competicao=competicao, status='P').count() == 0:
						solicitacao = Solicitacao()
						solicitacao.participante = user_participante
						solicitacao.competicao = competicao
						solicitacao.save()
						msg = 'Solicitacao enviada com sucesso, aguarde.'
						send_mail('Solicitacao', 'Solicitacao enviada: '+solicitacao.participante.apelido+' ... ' +SITE_ROOT+'solicitacoes/'+str(competicao.pk), 'diegolirio.dl@gmail.com', [competicao.presidente.user.email])
					else:
						msg = 'Solicitacao já enviada, aguarde...'
				else:
					msg = 'Você ja está inscrito nessa competição'
			else:
				msg = 'Para solicitar uma inscrição, termine seu cadastro. Confirme seu cadastro em seu Email'
		else:
			msg = 'Competição já encontra-se em andamento ou finalizada'
	else:
		msg = 'Realize o Login para realizar uma solicitação para participar'
	return render_to_response('_base.html', 
							{'template': 'solicita_inscricao.html', 
							 'message': msg, 
							 'user_participante': user_participante,
							 'competicao': competicao,
							'patrocinador': patrocinador,
							'publicidade': publicidade}
							 )

# Para o Presidente
@login_required
def minhas_competicoes(request):
	user_participante = get_participante_by_user(request.user)
	if Competicao.objects.filter(presidente=user_participante).count() <= 0:
		return redirect('/')
	competicoes = Competicao.objects.filter(presidente=user_participante)	
	return render_to_response('_base.html',{	'template': 'competicoes.html',
												'titulo': 'Minhas Competições',
												'subtitulo': '',
												'user_participante': user_participante,
												'url': '/solicitacoes/',
												'competicoes': competicoes
											})

# Para o Presidente											
@login_required
def solicitacoes(request, competicao_pk):
	user_participante = get_participante_by_user(request.user)
	competicao = Competicao.objects.get(pk=competicao_pk)
	user_inscricao = get_inscricao(competicao, user_participante)
	#print(request.GET['status'])
	try:
		status = request.GET['status']
	except:
		status = 'P'
	solicitacoes = Solicitacao.objects.filter(competicao=competicao,status=status)
	if user_participante.pk != competicao.presidente.pk:
		return redirect('/')
	return render_to_response('_base.html', 
	                          {    'template':'solicitacoes.html', 
								   'titulo': 'Solicitações',
	                               'subtitulo': competicao.nome,
	                               'user_participante': user_participante,
								   'user_inscricao': user_inscricao,
	                               'solicitacoes': solicitacoes,
	                               'competicao': competicao,
								   'message': 'None'
	                          })			

def __apostas_create_all__(participante, competicao):
	inscr = Inscricao.objects.filter(participante=participante, competicao=competicao)[0:1].get()
	grupos = Grupo.objects.filter(campeonato=competicao.campeonato)
	for g in grupos:
		jogos = Jogo.objects.filter(grupo=g)
		for j in jogos:
			aposta = Aposta()
			aposta.inscricao = inscr
			aposta.jogo = j
			if j.status.codigo == 'F':
				aposta.calculado = True
			aposta.save()			

def aceitar_solicitacao(request, solicitacao_pk):
	user_participante = get_participante_by_user(request.user)
	solicitacao = Solicitacao.objects.get(pk=solicitacao_pk)
	message = 'None'
	user_inscricao = Inscricao()
	if Inscricao.objects.filter(participante=solicitacao.participante, competicao=solicitacao.competicao).count() > 0:
		message = 'Já existe esse participante inscrito para esta competição'
	else:
		inscricao_new = Inscricao()
		inscricao_new.competicao = solicitacao.competicao
		inscricao_new.participante = solicitacao.participante
		inscricao_new.save()
		__apostas_create_all__(solicitacao.participante, solicitacao.competicao)
		solicitacao.status = 'A'
		solicitacao.save()
		user_inscricao = get_inscricao(solicitacao.competicao, user_participante)
		return redirect('/rancking/'+str(solicitacao.competicao.pk))
	solicitacoes = Solicitacao.objects.filter(pk=solicitacao_pk)
	return render_to_response('_base.html', 
	                          {    'template':'solicitacoes.html', 
								   'titulo': 'Solicitações',
	                               'subtitulo': solicitacao.competicao.nome,
	                               'user_participante': user_participante,
								   'user_inscricao': user_inscricao,
	                               'solicitacoes': solicitacoes,
	                               'competicao': solicitacao.competicao,
								   'message': message
	                          })	
							 
# begin system <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@login_required
def system(request):
	campeonatos = Campeonato.objects.all()
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base.html', {'template': 'system/index_campeonatos.html', 'titulo': 'Sistema', 'subtitulo': 'Campeonatos: Calcular e Alterar placar', 'user_participante': user_participante, 'campeonatos': campeonatos})

@login_required
def system_campeonato_calc_jogos(request, campeonato_pk):
	campeonato = Campeonato.objects.get(pk=campeonato_pk)
	#grupos = Grupo.objects.filter(campeonato=campeonato)
	#for g in grupos:
	#	jogos = Jogo.objects.filter(grupo=g)
	jogos = get_jogos_of_the_campeonato(campeonato)
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base.html', 
	                          {   'template': 'system/campeonato_calc_jogos.html', 
							      'titulo': 'Calcular ' + campeonato.nome, 
								  'subtitulo': 'Placar e calculo', 
								  'user_participante': user_participante, 
								  'campeonato': campeonato,
								  'jogos' : jogos})
								  
def system_novo_jogo(request, campeonato_pk):
	campeonato = Campeonato.objects.get(pk=campeonato_pk)
	grupos = Grupo.objects.filter(campeonato=campeonato)
	form = JogoForm()
	execute_transation = 'N'
	mensagem = ''
	if request.method == 'POST':
		form = JogoForm(request.POST, request.FILES)		
		if form.is_valid():
			jogo = form.save()
			competicoes = Competicao.objects.filter(campeonato=jogo.grupo.campeonato)
			for c in competicoes:
				inscricoes = Inscricao.objects.filter(competicao=c)
				for i in inscricoes:
					a = Aposta()
					a.inscricao = i
					a.jogo = jogo
					a.save()					
			execute_transation = 'S'
			mensagem = 'gravado com sucesso'
		else:
			print('form invalido')
	return render_to_response('_base_simple.html', {'template': 'system/novo_jogo.html', 'form': form, 'execute_transation': execute_transation, 'mensagem': mensagem, 'campeonato': campeonato, 'grupos': grupos}, context_instance=RequestContext(request))						  
								  
def system_jogo_edit(request, campeonato_pk, jogo_pk):
	campeonato = Campeonato.objects.get(pk=campeonato_pk)
	jogo = Jogo()
	form = JogoForm()
	execute_transation = 'N'
	mensagem = ''
	if request.method == 'POST':
		if jogo_pk != '0':
			jogo = Jogo.objects.get(pk=jogo_pk)
			form = JogoForm(request.POST, request.FILES, instance=jogo)		
		else:
			form = JogoForm(request.FILES, request.POST)		
		if form.is_valid():
			form.save()
			execute_transation = 'S'
			mensagem = 'Jogo alterado com sucesso!!!' if jogo_pk == '0' else 'Jogo gravado com sucesso!!!'
	else:
		if jogo_pk != '0':
			jogo = Jogo.objects.get(pk=jogo_pk)
			form = JogoForm(instance=jogo)
	return render_to_response('_base_simple.html', 
							  { 'template': 'jogo_edit.html',
                                'execute_transation': execute_transation,
	                            'campeonato': campeonato, 
								'jogo': jogo, 
	                            'form': form, 
	                            'mensagem': mensagem},
							  context_instance=RequestContext(request))	     

@login_required
def system_calcular_campeonato(request, campeonato_pk):
	envia_email = False
	campeonato = Campeonato.objects.get(pk=campeonato_pk)
	jogos = __get_jogos_not_edition_by_campeonato__(campeonato)
	for j in jogos:
		#print(j.time_a + " X " + j.time_b)
		__calcular_vencedor_jogo__(j)
		# calcula apostas e colocacao hist...
		__calcula_apostas__(j)
	# calcula somatorio definitivo
	competicoes = Competicao.objects.filter(campeonato=campeonato)
	for c in competicoes:
		inscricoes = Inscricao.objects.filter(competicao=c, ativo=True)
		for i in inscricoes:
			# somatorio na inscricao,
			__soma_pontuacao__(i)		
		#Calcula Rancking/colocacao
		__calcula_rancking__(c)
		# ToDo..: envia email
		#if envia_email:
		#	para todos os participante dessa competicao.
	return redirect('/home/')
	
@login_required		
def system_consultar_participante(request):
	user_participante = get_participante_by_user(request.user)
	participantes = Participante.objects.all()
	return render_to_response('_base.html', 
	                          {'template': 'system/consulta_participante.html', 
	                           'titulo': 'Consultar Participante', 
	                           'subtitulo': 'System',
	                           'user_participante': user_participante,
	                           'participantes': participantes
	                           }, RequestContext(request))	
		
	
@login_required	
def system_cadastrar_participante(request, participante_pk):
	message = ''
	status_transation = 'I'
	user_participante = get_participante_by_user(request.user)
	participante = Participante()
	form_user = UserNewForm()
	form_participante = ParticipanteAdminForm()	
	participante = Participante()
	if request.method == 'POST':
		if participante_pk == '0':
			form_user = UserNewForm(request.POST, request.FILES)
			if form_user.is_valid():
				user = form_user.save()
				participante = __new_participante__(user)
				emailss = [user.email,]
				send_mail('Conrfimacao de cadastro '+NOME_BOLAO, 'Usuario: '+ user.username +', clique no link para confirmar o cadastro ' + SITE_ROOT + 'confirm_email/'+participante.confirm_send_code+ '/?user='+str(user.pk), 'diegolirio.dl@gmail.com', emailss)
				return redirect('/system/cadastrar_participante/'+str(user.pk))	
		else:
			participante = Participante.objects.get(pk=participante_pk)
			if 'save_user' in request.POST:
				form_user = UserEditForm(request.POST, request.FILES, instance=participante.user)
				form_participante = ParticipanteAdminForm(instance=participante)	
				if form_user.is_valid():
					form_user.save()
					message = u'Informações de usuário gravado com sucesso!'
					#return redirect('/cadastre_se/')
			elif 'save_participante' in request.POST:
				form_participante = ParticipanteAdminForm(request.POST, request.FILES, instance=participante)
				form_user = UserEditForm(instance=participante.user)
				if form_participante.is_valid():	
					form_participante.save()
					message = u'Informações de participante gravado com sucesso!'
			status_transation = 'V'		
	else:
		if participante_pk != '0':
			participante = Participante.objects.get(pk=participante_pk)
			form_user = UserEditForm(instance=participante.user)
			if user_participante != None:
				form_participante = ParticipanteAdminForm(instance=participante)	
			status_transation = 'V'		
	return render_to_response('_base.html', 
	                          {'template': 'system/cadastrar_participante.html', 
	                           'titulo': 'Cadastro System', 
	                           'subtitulo': '',
	                           'user_participante': user_participante,
	                           'form_user': form_user,
							   'form_participante': form_participante,
							   'participante': participante,
							   'status_transation': status_transation,
							   'message': message
	                           }, RequestContext(request))	
							   
def system_inscricoes_participante(request, participante_pk):
	participante = Participante.objects.get(pk=participante_pk)
	user_participante = get_participante_by_user(request.user)
	minhas_inscricoes = Inscricao.objects.filter(participante=participante)
	competicoes_all = Competicao.objects.all()
	outras_competicoes = list()
	include = True
	for c in competicoes_all:
		for mi in minhas_inscricoes:
			if c == mi.competicao:
				include = False
				break
		if include:
			outras_competicoes.append(c)
		include = True
	return render_to_response('_base_simple.html', 
	                          {'template': 'system/inscricoes_participante.html', 
	                           'user_participante': user_participante,
							   'minhas_inscricoes': minhas_inscricoes,
							   'outras_competicoes': outras_competicoes,
							   'participante': participante
	                           }, RequestContext(request))	

def get_ultima_colocacao_rodada(competicao, jogo):
	max = 0
	inscricoes = Inscricao.objects.filter(competicao=competicao)
	for i in inscricoes:
		apostas_ = Aposta.objects.filter(inscricao=i)
		for a in apostas_:
			if a.jogo == jogo:
				if a.colocacao > max:
					max = a.colocacao
	return max
	                           
def system_inscrever_participante_competicao(request, participante_pk, competicao_pk):
	user_participante = get_participante_by_user(request.user)
	participante = Participante.objects.get(pk=participante_pk)
	competicao = Competicao.objects.get(pk=competicao_pk)
	execute_transation = 'N'
	mensagem = ''
	if Inscricao.objects.filter(competicao=competicao, participante=participante).count() == 0:
		inscricao = Inscricao()
		inscricao.competicao = competicao
		inscricao.participante = participante
		#inscricao.colocacao = max()+1 # Calcular novamente
		inscricao.save()		
		grupos = Grupo.objects.filter(campeonato=competicao.campeonato)
		qtde_nao_participou = 0
		for g in grupos:
			jogos = Jogo.objects.filter(grupo=g)
			for j in jogos:
				a = Aposta()
				a.jogo = j
				a.inscricao = inscricao
				if j.status.codigo == 'F' or j.status.codigo == 'A':
					a.calculado = True
					a.riscado = True
					a.colocacao = get_ultima_colocacao_rodada(competicao, j)
					qtde_nao_participou += 1
				a.save()
		inscricao.nao_participou = qtde_nao_participou
	return redirect('/system/inscricoes_participante/'+str(participante.pk))		
	
def set_ativo_participante_competicao(ativo, inscricao):
	inscricao.ativo = ativo
	inscricao.save()
							   
def system_desativar_participante_competicao(request, inscricao_pk):
	user_participante = get_participante_by_user(request.user)
	inscricao = Inscricao.objects.get(pk=inscricao_pk)
	set_ativo_participante_competicao(False, inscricao)
	return redirect('/system/inscricoes_participante/'+str(inscricao.participante.pk))	
							   
def system_ativar_participante_competicao(request, inscricao_pk):
	user_participante = get_participante_by_user(request.user)
	inscricao = Inscricao.objects.get(pk=inscricao_pk)
	set_ativo_participante_competicao(True, inscricao)
	return redirect('/system/inscricoes_participante/'+str(inscricao.participante.pk))							   
							   
def system_patrocinadores_por_competicao(request):
	user_participante = get_participante_by_user(request.user)
	competicoes = Competicao.objects.all()	
	return render_to_response('_base.html', 
	                          {'template': 'system/patrocinadores_por_competicao.html', 
	                           'titulo': 'Gerenciar Patrocinios ', 
	                           'subtitulo': u'Competicoes',
	                           'user_participante': user_participante,
							   'competicoes': competicoes
	                           }, RequestContext(request))	

def system_paginas_publicidade(request, competicao_pk):
	user_participante = get_participante_by_user(request.user)
	competicao = Competicao.objects.get(pk=competicao_pk)
	paginas = Pagina.objects.all()
	patrocinador = __get_patrocinador_principal__(competicao)
	return render_to_response('_base.html', 
	                          {'template': 'system/paginas.html', 
	                           'titulo': 'Paginas de Publicidade', 
	                           'subtitulo': 'Copa ' + patrocinador.patrocinador.nome_visual + ' ' + competicao.nome,
	                           'user_participante': user_participante,
							   'competicao': competicao,
							   'paginas': paginas
	                           }, RequestContext(request))	
							   
def system_publicidade_pagina(request, competicao_pk, pagina_pk):
	user_participante = get_participante_by_user(request.user)
	pagina = Pagina.objects.get(pk=pagina_pk)
	competicao = Competicao.objects.get(pk=competicao_pk)
	patrocinador = __get_patrocinador_principal__(competicao)
	
	patrocinadores_pagina = list()
	patrocinadores_pagina_aux = PaginaPatrocinio.objects.filter(pagina=pagina)	
	for pp in patrocinadores_pagina_aux:
		if pp.competicacao_patrocinador.competicao == competicao:
			patrocinadores_pagina.append(pp)

	if (pagina.codigo_pagina == 'R') or (pagina.codigo_pagina == 'T'):
		patrocinadores_competicao_aux = Competicao_Patrocinadores.objects.filter(competicao=competicao).exclude(principal=True)
	else:
		patrocinadores_competicao_aux = Competicao_Patrocinadores.objects.filter(competicao=competicao)
		
	patrocinadores_competicao = list()		
	include = True
	for pc in patrocinadores_competicao_aux:
		for pp in patrocinadores_pagina:
			if pp.competicacao_patrocinador.patrocinador.pk == pc.patrocinador.pk:
				include = False
				break
		if include:
			patrocinadores_competicao.append(pc)
		include = True
	return render_to_response('_base.html', 
	                          {'template': 'system/publicidade_pagina.html', 
	                           'titulo': 'Pagina ' + pagina.nome_pagina,
	                           'subtitulo': 'Copa ' + patrocinador.patrocinador.nome_visual + ' ' + competicao.nome,
	                           'user_participante': user_participante,
							   'competicao': competicao,
							   'pagina': pagina,
							   'patrocinadores_competicao': patrocinadores_competicao,
							   'patrocinadores_pagina': patrocinadores_pagina
	                           }, RequestContext(request))		
							   
def system_retirar_patrocinio_pagina(request, patrocinador_pagina_pk):
	pag_patro = PaginaPatrocinio.objects.get(pk=patrocinador_pagina_pk)
	pag_patro.delete()
	return redirect('/system/publicidade_pagina/'+str(pag_patro.competicacao_patrocinador.competicao.pk)+'/'+str(pag_patro.pagina.pk)+'/')
	
def system_incluir_patrocinio_pagina(request, pagina_pk, patrocinador_competicao_pk):
	pagina = Pagina.objects.get(pk=pagina_pk)
	competicao_patrocinador = Competicao_Patrocinadores.objects.get(pk=patrocinador_competicao_pk)
	pag_patro = PaginaPatrocinio()
	pag_patro.pagina = pagina
	pag_patro.competicacao_patrocinador = competicao_patrocinador
	
	if pagina.qtde_total_patrocinio == 1:
		pag_patro_del = PaginaPatrocinio.objects.filter(pagina=pagina)
		for ppd in pag_patro_del:
			ppd.delete()
	pag_patro.save()
	return redirect('/system/publicidade_pagina/'+str(pag_patro.competicacao_patrocinador.competicao.pk)+'/'+str(pag_patro.pagina.pk)+'/')

def system_competicao_publicidade(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)
	patrocinador = __get_patrocinador_principal__(competicao)
	user_participante = get_participante_by_user(request.user)
	patrocinadores = Competicao_Patrocinadores.objects.filter(competicao=competicao).order_by('-principal')
	return render_to_response('_base.html', 
	                          {'template': 'system/competicao_publicidade.html', 
	                           'titulo': 'Patrocinadores ',
	                           'subtitulo': 'Copa ' + patrocinador.patrocinador.nome_visual + ' ' + competicao.nome,
	                           'user_participante': user_participante,
							   'competicao': competicao,
							   'patrocinadores': patrocinadores
	                           }, RequestContext(request))

def system_novo_patrocinador_competicao(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)
	patrocinadores_c = Competicao_Patrocinadores.objects.filter(competicao=competicao).order_by('-principal')
	patrocinadores_all = Patrocinador.objects.all()
	patrocinadores = list()
	patrocina = False
	for p_all in patrocinadores_all:
		for p_c in patrocinadores_c:
			if p_all == p_c.patrocinador:
				patrocina = True
				break
		if not patrocina:
			patrocinadores.append(p_all)
		patrocina = False
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base_simple.html', 
	                          {'template': 'system/novo_patrocinador_competicao.html', 
	                           'user_participante': user_participante,
							   'patrocinadores': patrocinadores,
							   'competicao': competicao
	                           }, RequestContext(request))	
							   
def system_incluir_patrocinador_competicao(request, competicao_pk, patrocinador_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)
	patrocinador = Patrocinador.objects.get(pk=patrocinador_pk)
	competicao_patrocinador = Competicao_Patrocinadores()
	competicao_patrocinador.competicao = competicao
	competicao_patrocinador.patrocinador = patrocinador
	competicao_patrocinador.save()
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base_simple.html', 
	                          {'template': 'system/novo_patrocinador_competicao.html', 
	                           'user_participante': user_participante,
							   #'patrocinadores': patrocinadores,
							   'competicao': competicao,
							   'mensagem': u'Patrocinador incluído com sucesso para a Competição',
							   'execute_transation': 'S'
	                           }, RequestContext(request))								   
							   
def system_retirar_patrocinador_competicao(request, competicao_patrocinador_pk):
	competicao_patrocinador = Competicao_Patrocinadores.objects.get(pk=competicao_patrocinador_pk)
	competicao = competicao_patrocinador.competicao
	competicao_patrocinador.delete()
	user_participante = get_participante_by_user(request.user)
	return redirect('/system/competicao_publicidade/'+str(competicao.pk)+'/')
							   
@login_required							   
def system_send_mail_all(request, campeonato_pk):
	user_participante = get_participante_by_user(request.user)
	
	campeonato = Campeonato.objects.get(pk=campeonato_pk)
	print(campeonato.nome)
	competicoes = Competicao.objects.filter(campeonato=campeonato)
	for c in competicoes:
		print(c.nome)
		inscricoes = Inscricao.objects.filter(competicao=c)
		url_email_rancking = SITE_ROOT + 'rancking/'+str(c.pk)+'/'
		for i in inscricoes:
			print('Enviado email >>> ' + i.participante.apelido)
			i.participante.user.email_user('Rancking Atualizado', u'Olá ' + i.participante.apelido + u', segue o rancking atualizado do Bolão >>>> ' + url_email_rancking, from_email=None)	
	return render_to_response('_base.html',
								{ 'template': 'system/email_enviado.html',
								  'titulo': 'Email',
								  'subtitulo': '',
								  'mensagem': 'Email enviado com sucesso!',
								  'user_participante': user_participante })
								  
	
def __calcular_vencedor_jogo__(j):
	if j.resultado_a > j.resultado_b:
		j.vencedor = 'A'
	elif j.resultado_a < j.resultado_b:
		j.vencedor = 'B'
	else:
		j.vencedor = 'E'
	j.save()	
	
def __calcula_apostas__(jogo):
	apostas = Aposta.objects.filter(jogo=jogo, calculado=False)
	if apostas.count():
		competicao = apostas[0].inscricao.competicao
	i = 0
	for a in apostas:
		i = i + 1
		if (a.resultado_a == jogo.resultado_a) and (a.resultado_b == jogo.resultado_b):
			a.pontos = PONTOS_PLACAR
		elif (a.vencedor == jogo.vencedor) and (a.vencedor != 'E') and ((a.resultado_a == jogo.resultado_a) or (a.resultado_b == jogo.resultado_b)):
			a.pontos = PONTOS_VENCEDOR_RESULTADO_GOLS_UM_TIME
		elif (a.vencedor == jogo.vencedor) and (a.vencedor != 'E'):
			a.pontos = PONTOS_VENCEDOR
		elif (a.vencedor == jogo.vencedor) and (a.vencedor == 'E'):
			a.pontos = PONTOS_EMPATE_PLACAR_INCORRETO
		elif (a.vencedor != jogo.vencedor) and ((a.resultado_a == jogo.resultado_a) or (a.resultado_b == jogo.resultado_b)):
			a.pontos = PONTOS_SOMENTE_RESULTADO_GOLS_UM_TIME
		else:
			a.pontos = PONTOS_ERRO
		# somente entre no blobo if abaixo os Finalizados com nao calculados
		if a.jogo.status.codigo == 'F':
			a.calculado = True
			a.colocacao = -1
			envia_email = True
		elif a.jogo.status.codigo == 'A':
			a.colocacao = -1
		a.save()
		if (competicao != a.inscricao.competicao) or (i == apostas.count()):
			competicao = a.inscricao.competicao
			# calcula colocacao na aposta (competicao)
			__calcula_colocacao_aposta__(competicao)
		
# RANCKING		
def __calcula_colocacao_aposta__(competicao):
	inscricoes_soma = Inscricao.objects.filter(competicao=competicao)
	for i_ in inscricoes_soma:
		# somatorio e depois o rancking
		__soma_pontuacao__(i_)
	# rancking hist eh feito na inscricao no calculado, que provalvelmente sera refeito novamente ao sair do __calcula_apostas__
	__calcula_rancking__(competicao)
	# filtrar novamente as inscricoes ja alteradas a colocacao...
	inscricoes_colocacao = Inscricao.objects.filter(competicao=competicao)
	for i in inscricoes_colocacao:	
		apostas = Aposta.objects.filter(inscricao=i, colocacao=-1)
		for a in apostas:
			a.colocacao = i.colocacao
			a.save()
		
# Soma a pontuacao toda vez que calcula....
def __soma_pontuacao__(inscricao):
	# ToDo...: Cria metodo separa para o calculo somatorio. Passando a inscricao como parametro.
	apostas = Aposta.objects.filter(inscricao=inscricao)
	qtde_ap = 0
	qtde_ar = 0
	qtde_av = 0
	qtde_ae = 0
	qtde_as = 0					
	qtde_er = 0					
	pt = 0
	for a in apostas:
		if a.jogo.status.codigo != 'E':
			pt = pt + a.pontos
			if a.pontos == PONTOS_PLACAR:
				qtde_ap = qtde_ap + 1	
			if a.pontos == PONTOS_VENCEDOR_RESULTADO_GOLS_UM_TIME:
				qtde_ar = qtde_ar + 1						
			elif a.pontos == PONTOS_VENCEDOR:
				qtde_av = qtde_av + 1
			elif a.pontos == PONTOS_EMPATE_PLACAR_INCORRETO:
				qtde_ae = qtde_ae + 1	
			elif a.pontos == PONTOS_SOMENTE_RESULTADO_GOLS_UM_TIME:
				qtde_as = qtde_as + 1	
			elif (a.jogo.status.codigo != 'E') and (a.pontos == PONTOS_ERRO):
				qtde_er = qtde_er + 1
	inscricao.pontos = pt
	inscricao.quantidade_acerto_placar = qtde_ap
	inscricao.quantidade_acerto_vencedor_um_resultado_correto = qtde_ar
	inscricao.quantidade_acerto_vencedor = qtde_av
	inscricao.quantidade_acerto_empate_erro_placar = qtde_ae
	inscricao.quantidade_acerto_somente_resultado_um_time = qtde_as
	inscricao.quantidade_erro = qtde_er
	inscricao.save()		
	return inscricao

def __limpa_pontuacao__(inscricao):
	inscricao.pontos = 0
	inscricao.quantidade_acerto_placar = 0
	inscricao.quantidade_acerto_vencedor_um_resultado_correto = 0
	inscricao.quantidade_acerto_vencedor = 0
	inscricao.quantidade_acerto_empate_erro_placar = 0
	inscricao.quantidade_acerto_somente_resultado_um_time = 0
	inscricao.quantidade_erro = 0
	inscricao.save()			

#Calcula Rancking/colocacao
def __calcula_rancking__(competicao):
	inscricoes = Inscricao.objects.filter(competicao=competicao, ativo=True).order_by('-pontos','-quantidade_acerto_placar', '-quantidade_acerto_vencedor_um_resultado_correto', '-quantidade_acerto_vencedor','-quantidade_acerto_empate_erro_placar', '-quantidade_acerto_somente_resultado_um_time')
	col_inc_ = 0
	col_real = 0
	pt_anterior = 0
	qtde_ap = 0
	qtde_ar = 0
	qtde_av = 0
	qtde_ae = 0
	qtde_as = 0
	for i in inscricoes:
		col_inc_ = col_inc_ + 1		
		if (i.pontos != pt_anterior) or (i.quantidade_acerto_vencedor_um_resultado_correto != qtde_ar) or (i.quantidade_acerto_placar != qtde_ap) or (i.quantidade_acerto_vencedor != qtde_av) or (i.quantidade_acerto_empate_erro_placar != qtde_ae) or (i.quantidade_acerto_somente_resultado_um_time != qtde_as):			
			col_real = col_inc_
			i.colocacao = col_real
		else:
			i.colocacao = col_real
		i.save()
		pt_anterior = i.pontos
		qtde_ap = i.quantidade_acerto_placar
		qtde_ar = i.quantidade_acerto_vencedor_um_resultado_correto
		qtde_av = i.quantidade_acerto_vencedor
		qtde_ae = i.quantidade_acerto_empate_erro_placar
		qtde_as = i.quantidade_acerto_somente_resultado_um_time
		
# end system	<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<




	
# Faz o Calculo do campeonato para todas as competicoes do mesmo.
@login_required
def aposta_calc(request, campeonato):
	c = Campeonato.objects.get(pk=campeonato)
	grupos = Grupo.objects.filter(campeonato=c)
	for g in grupos:
		jogos = Jogo.objects.filter(grupo=g).order_by('data_hora')
		for j in jogos:
			# Calcular Vencedor
			calcular_vencedor_jogo(j) 
			# Calcula todas as apostas de todos os participantes com este jogo, se estiver finalizado
			#if j.status.codigo != 'E':
			calcula_aposta(j) 
	
	competicoes = Competicao.objects.filter(campeonato=c)
	for co in competicoes:
		# Calcula pontuacao na inscricao que contem a soma da pontuacao
		inscricoes = Inscricao.objects.filter(competicao=co)
		for i in inscricoes:
			calcula_soma_pontos(i)
		#Calcula Rancking/colocacao
		calcula_rancking(co)			
	return redirect('/home/')

# calcula a aposta.
def calcula_aposta(jogo):
	# pega somente as apostas não calculadas
	apostas = Aposta.objects.filter(jogo=jogo, calculado=False)	
	# >>> To: Rancking historico
	"""
	if apostas.count() > 0:
		competicao = apostas[0].inscricao.competicao
	i = 0
	"""
	# >>>	
	for a in apostas:
		if a.jogo.status != 'E':
			if (a.resultado_a == jogo.resultado_a) and (a.resultado_b == jogo.resultado_b):
				a.pontos = PONTOS_PLACAR
			elif (a.vencedor == jogo.vencedor) and (a.vencedor != 'E') and ((a.resultado_a == jogo.resultado_a) or (a.resultado_b == jogo.resultado_b)):
				a.pontos = PONTOS_VENCEDOR_RESULTADO_GOLS_UM_TIME
			elif (a.vencedor == jogo.vencedor) and (a.vencedor != 'E'):
				a.pontos = PONTOS_VENCEDOR
			elif (a.vencedor == jogo.vencedor) and (a.vencedor == 'E'):
				a.pontos = PONTOS_EMPATE_PLACAR_INCORRETO
			elif (a.vencedor != jogo.vencedor) and ((a.resultado_a == jogo.resultado_a) or (a.resultado_b == jogo.resultado_b)):
				a.pontos = PONTOS_SOMENTE_RESULTADO_GOLS_UM_TIME
			else:
				a.pontos = PONTOS_ERRO
			if a.jogo.status.codigo == 'F':
				a.calculado = True
		else:
			a.pontos = 0
			a.calculado = False
			a.colocacao = 0
		a.save()
		
		# calcula o rancking no momento da aposta (historico de colocacao)
		"""
		i = i + 1	
		if (i == apostas.count()) or (competicao != a.inscricao.competicao):
			#print('Calculando >>>>>> ' + competicao.nome + ' <> ' + str(i)+' de '+ str(apostas.count()))
			calcula_rancking_historico(competicao, jogo, a)
			competicao = a.inscricao.competicao
		"""
		
def calcula_soma_pontos(inscricao):
	# ToDo...: Cria metodo separa para o calculo somatorio. Passando a inscricao como parametro.
	apostas = Aposta.objects.filter(inscricao=inscricao)
	qtde_ap = 0
	qtde_ar = 0
	qtde_av = 0
	qtde_ae = 0
	qtde_as = 0					
	qtde_er = 0					
	pt = 0
	for a in apostas:
		pt = pt + a.pontos
		if a.pontos == PONTOS_PLACAR:
			qtde_ap = qtde_ap + 1	
		if a.pontos == PONTOS_VENCEDOR_RESULTADO_GOLS_UM_TIME:
			qtde_ar = qtde_ar + 1						
		elif a.pontos == PONTOS_VENCEDOR:
			qtde_av = qtde_av + 1	
		elif a.pontos == PONTOS_EMPATE_PLACAR_INCORRETO:
			qtde_ae = qtde_ae + 1	
		elif a.pontos == PONTOS_SOMENTE_RESULTADO_GOLS_UM_TIME:
			qtde_as = qtde_as + 1	
		elif (a.jogo.status.codigo != 'E') and (a.pontos == PONTOS_ERRO):
			qtde_er = qtde_er + 1
	inscricao.pontos = pt
	inscricao.quantidade_acerto_placar = qtde_ap
	inscricao.quantidade_acerto_vencedor_um_resultado_correto = qtde_ar
	inscricao.quantidade_acerto_vencedor = qtde_av
	inscricao.quantidade_acerto_empate_erro_placar = qtde_ae
	inscricao.quantidade_acerto_somente_resultado_um_time = qtde_as
	inscricao.quantidade_erro = qtde_er
	inscricao.save()		
	
def soma_aposta_inscricao(inscricao, aposta):
	inscricao_ = inscricao
	inscricao_.pontos = inscricao_.pontos + aposta.pontos
	if aposta.pontos == PONTOS_PLACAR:
		inscricao_.quantidade_acerto_placar = inscricao_.quantidade_acerto_placar + 1
	if aposta.pontos == PONTOS_VENCEDOR_RESULTADO_GOLS_UM_TIME:
		inscricao_.quantidade_acerto_vencedor_um_resultado_correto = inscricao_.quantidade_acerto_vencedor_um_resultado_correto + 1
	elif aposta.pontos == PONTOS_VENCEDOR:
		inscricao_.quantidade_acerto_vencedor = inscricao_.quantidade_acerto_vencedor + 1
	elif aposta.pontos == PONTOS_EMPATE_PLACAR_INCORRETO:
		inscricao_.quantidade_acerto_empate_erro_placar = inscricao_.quantidade_acerto_empate_erro_placar + 1
	elif aposta.pontos == PONTOS_SOMENTE_RESULTADO_GOLS_UM_TIME:
		inscricao_.quantidade_acerto_somente_resultado_um_time = inscricao_.quantidade_acerto_somente_resultado_um_time + 1
	elif (aposta.jogo.status.codigo != 'E') and (aposta.pontos == PONTOS_ERRO):
		inscricao_.quantidade_erro = inscricao_.quantidade_erro + 1
	return inscricao_
		
#Calcula Rancking/colocacao na aposta (Histórico)
def calcula_rancking_historico(competicao, jogo, aposta):
	inscricoes_calc = Inscricao.objects.filter(competicao=competicao).order_by('-pontos','-quantidade_acerto_placar', '-quantidade_acerto_vencedor_um_resultado_correto', '-quantidade_acerto_vencedor','-quantidade_acerto_empate_erro_placar', '-quantidade_acerto_somente_resultado_um_time')
	col = 0
	pt_anterior = 0
	qtde_ap = 0
	qtde_av = 0
	qtde_ae = 0
	inscricoes = list()
	# ToDo...: Calcula Aposta atual do Jogo com o que esta na inscricao.
	for i_ in inscricoes_calc:
		i_calculado = soma_aposta_inscricao(i_, aposta)	
		inscricoes.append(i_calculado)
	for i in inscricoes:
		col = col + 1		
		if (i.pontos != pt_anterior) or (i.quantidade_acerto_placar != qtde_ap) or (i.quantidade_acerto_vencedor != qtde_av) or (i.quantidade_acerto_empate_erro_placar != qtde_ae):			
			i.colocacao = col
		else:
			i.colocacao = col-1
		pt_anterior = i.pontos
		qtde_ap = i.quantidade_acerto_placar
		qtde_av = i.quantidade_acerto_vencedor
		qtde_ae = i.quantidade_acerto_empate_erro_placar
		# rancking no momento da Aposta
		a = Aposta.objects.filter(jogo=jogo, inscricao=i)[0:1].get()
		a.colocacao = i.colocacao
		a.save()
		
def patrocinadores(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)
	patrocinadores = Competicao_Patrocinadores.objects.filter(competicao=competicao)
	patrocinador = __get_patrocinador_principal__(competicao)
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	return render_to_response('_base.html', 
	                          {    'template':'patrocinadores.html', 
								   'titulo': 'Patrocinadores',
	                               'subtitulo': u'Competição: Copa ' + competicao.nome,
	                               'user_participante': user_participante,
								   'user_inscricao': user_inscricao,
	                               'patrocinadores': patrocinadores,
								   'patrocinador': patrocinador,
	                               'competicao': competicao
	                          })				
	
		
def regras(request):
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base.html', 
	                          {   'template': 'regras.html', 
							      'titulo': 'Regras ', 
								  'subtitulo': 'Regras', 
								  'user_participante': user_participante})						  

def lembrar_senha(request):
	execute_transation = 'N'
	mensagem = ''
	user = User()
	if request.method == 'POST':
		form = UserPasswordForm(request.POST, request.FILES)
		user_name = form['username'].value
		user = User.objects.get(username=user_name)
		participante = Participante.objects.filter(user=user)[0:1].get()
		#if participante.code_new_password != '0':
		participante.code_new_password = __get_code_random__()
		participante.save()
		url_email_ = SITE_ROOT + 'redefinir_senha/'+str(user.pk)+'/'+participante.code_new_password+'/?Redefinindo_senha_______=2014'
		user.email_user('Redefinir de Senha', u'Olá ' + user.username + u', para redefinir sua senha clique no link a seguir ' + url_email_, from_email=None)	
		execute_transation = 'S'
		mensagem = U'Sua senha será redefina após acessar um link enviado ao seu email !!!'
	return render_to_response('_base_simple.html', 
							  { 'template': 'lembrar_senha.html',
                                'execute_transation': execute_transation,
	                            'user': user, 
	                            'mensagem': mensagem},
							  context_instance=RequestContext(request))	
							  
def redefinir_senha(request, user_pk, code_new_password):
	user = User.objects.get(pk=user_pk)
	participante = Participante.objects.filter(user=user)[0:1].get()
	titulo__ = u'Redefinição de senha'
	form_user = UserRedefineForm()
	redefinindo = 'N'	
	if request.method == 'POST':		
		form_user = UserRedefineForm(request.POST, request.FILES, instance=user)
		if form_user.is_valid():
			form_user.save()	
			titulo__ = 'Senha redefinida com sucesso'
		else:
			redefinindo = 'S'
	else:
		if participante.code_new_password == code_new_password:
			participante.code_new_password = '0'
			participante.save()
			form_user = UserRedefineForm()
			redefinindo = 'S'
		else:
			titulo__ = u'Não foi possivel localizar usuario'
	return render_to_response('_base.html', 
	                          {    'template':'redefinir_senha.html', 
								   'titulo': titulo__,
	                               'subtitulo': '',
								   'form_user': form_user,
								   'user': user,
								   'redefinindo': redefinindo
	                          }, RequestContext(request))		
							  
def logout(request):
	form = UserPasswordForm()
	patrocinador_out = __get_one_puclicidade_global__('O')
	return render_to_response('login.html', 
							  {     #'template': 'login.html',
									'form': form,
									'log': 'out',
									'patrocinador_out': patrocinador_out
							        }, RequestContext(request))	
