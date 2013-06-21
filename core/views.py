# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from core.const import *
from core.models import *
from core.forms import *
#import datetime

def user_login_is_valid(user_request, user_inscricao):
	if user_request.pk == user_inscricao.pk:
		return True
	return False
	
def get_participante_by_user(user):
	user_participante = Participante()
	if user.is_authenticated():
		try:
			user_participante = Participante.objects.filter(user=user)[0:1].get()
		except:
			return redirect('/cadastre_se/')
	return user_participante			
	
def home(request):
	competicoes = Competicao.objects.all()	
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base.html',{	'template': 'index.html',
												'titulo': 'Troféu Bolão',
												'subtitulo': '',
												'user_participante': user_participante,
												'competicoes': competicoes
											})
											
def get_rancking_by_competicao(competicao):
	return Inscricao.objects.filter(competicao=competicao).order_by('colocacao')
	
def get_inscricao(competicao, participante):
	try:
		user_inscricao = Inscricao.objects.filter(competicao=competicao, participante=participante)[0:1].get()
	except:
		user_inscricao = Inscricao()	
	return user_inscricao

def set_properties(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)


def rancking(request, competicao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	inscricoes_competicao = get_rancking_by_competicao(competicao)
	return render_to_response('_base.html', 
							  {     'template': 'rancking.html', 
							        'titulo': 'Rancking', 
							        'subtitulo': competicao.campeonato.nome + ' ' + competicao.nome,
							        'user_participante': user_participante,
							        'user_inscricao': user_inscricao,
							        'competicao': competicao,
							        #-----------------------------------
							        'inscricoes_competicao': inscricoes_competicao
							        })
"""
@login_required
def irancking(request, user_inscricao_pk):
	user_inscricao = Inscricao.objects.get(pk=user_inscricao_pk)
	if not user_login_is_valid(request.user, user_inscricao.participante.user):
		return redirect('/')
	inscricoes_competicao = get_rancking_by_competicao(user_inscricao.competicao)		
	return render_to_response('_base.html', 
	                         {      'template': 'rancking.html', 
	                                'titulo': 'Rancking', 
	                                'subtitulo': user_inscricao.competicao.campeonato.nome + ' ' + user_inscricao.competicao.nome,
	                                'inscricoes_competicao': inscricoes_competicao, 
									# Sempre conter esses para pegar os dados de ambos
	                                'user_participante': user_inscricao.participante,
	                                'user_inscricao': user_inscricao,
	                                'competicao': user_inscricao.competicao,
									# url privadas contem inscricao da competicacao
							        'nome_rancking': NOME_RANCKING,
							        'url_rancking': URL_IRANCKING + str(user_inscricao.pk)+'/',
							        'nome_tabela': NOME_TABELA,
							        'url_tabela': URL_ITABELA + str(user_inscricao.pk)+'/',
							        'nome_aposta': NOME_APOSTA,
							        'url_aposta': URL_IAPOSTA + str(user_inscricao.pk)+'/',
							        'nome_perfil_competicao': '',
							        'url_perfil_competicao': URL_IPERFIL_COMPETICAO + str(user_inscricao.pk)+'/'
	                                })
"""
	                                
def get_jogos_of_the_campeonato(campeonato):
	grupos = Grupo.objects.all().filter(campeonato=campeonato)
	jgs = []
	for g in grupos:
		js = Jogo.objects.filter(grupo=g).order_by('data_hora')
		for j in js:
			jgs.append(j)
	return jgs			                                

def tabela(request, competicao_pk):	
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	jgs = get_jogos_of_the_campeonato(competicao.campeonato)
	return render_to_response('_base.html', 
							  {       'template': 'tabela.html', 
								      'titulo': 'Tabela',
								      'subtitulo': competicao.campeonato.nome + ' ' + competicao.nome,
								      'user_participante': user_participante,
								      'user_inscricao': user_inscricao,
								      'competicao': competicao,
								      #----
									  'jogos': jgs
							 })
"""
@login_required
def itabela(request, user_inscricao_pk):
	user_inscricao = Inscricao.objects.get(pk=user_inscricao_pk)
	if not user_login_is_valid(request.user, user_inscricao.participante.user):
		return redirect('/')
	jgs = get_jogos_of_the_campeonato(user_inscricao.competicao.campeonato)
	return render_to_response('_base.html', 
							  {       'template': 'tabela.html', 
								      'titulo': 'Tabela', 
								      'subtitulo': user_inscricao.competicao.campeonato.nome + ' ' + user_inscricao.competicao.nome,
								      'competicao': user_inscricao.competicao,
									  'jogos': jgs, 
									  'user_participante': user_inscricao.participante,
									  'user_inscricao': user_inscricao, 
									  # url privadas contem inscricao da competicacao
							          'nome_rancking': NOME_RANCKING,
							          'url_rancking': URL_IRANCKING + str(user_inscricao.pk)+'/',
							          'nome_tabela': NOME_TABELA,
							          'url_tabela': URL_ITABELA + str(user_inscricao.pk)+'/',
							          'nome_aposta': NOME_APOSTA,
							          'url_aposta': URL_IAPOSTA + str(user_inscricao.pk)+'/',
									  'nome_apostas_jogo': NOME_APOSTAS_JOGO,
									  'url_apostas_jogo': URL_IAPOSTAS_JOGO + str(user_inscricao.pk)+'/'							          
							 })
"""

def get_palpites_all_participantes(jogo, competicao):
	apostas = Aposta.objects.filter(jogo=jogo).order_by('-pontos')
	inscricoes = Inscricao.objects.filter(competicao=competicao)	
	apostas_jogos_competicao = []	
	for a in apostas:
		for i in inscricoes:
			if a.inscricao.pk == i.pk:
				apostas_jogos_competicao.append(a)		
	return apostas_jogos_competicao

# apostas de um soh jogo e competicao Ex: Brasil X Italia (Copa do Mundo 2014 - Della Volpe)
def apostas_jogo(request, competicao_pk, jogo_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	jogo = Jogo.objects.get(pk=jogo_pk)
	if (jogo.status.codigo == 'E'):
		return redirect(URL_TABELA+str(competicao.pk)+'/')		
	apostas_jogos_competicao = get_palpites_all_participantes(jogo, competicao)
	return render_to_response('_base.html', 
	                          {   'template': 'apostas_jogo.html', 
								  'titulo': 'Palpites de Todos',
								  'subtitulo': competicao.campeonato.nome + ' ' + competicao.nome,
								  'user_participante': user_participante,
								  'user_inscricao': user_inscricao,
								  'competicao': competicao,								  
	                              'jogo': jogo, 
	                              'apostas': apostas_jogos_competicao
	                           })	


"""
# Visualiza as apostas daquele expecifico Jogo e Competicao
@login_required
def iapostas_jogo(request, user_inscricao_pk, jogo_pk):
	user_inscricao = Inscricao.objects.get(pk=user_inscricao_pk)
	if not user_login_is_valid(request.user, user_inscricao.participante.user):
		return redirect('/')
	j = Jogo.objects.get(pk=jogo_pk)	
	if (j.status.codigo == 'E'):
		return redirect(URL_ITABELA+str(user_inscricao.pk)+'/')	
	# apostas de um soh jogo e competicao Ex: Brasil X Italia (Copa do Mundo 2014 - Della Volpe)
	apostas_jogos_competicao = get_palpites_all_participantes(j, user_inscricao.competicao)
	return render_to_response('_base.html', 
	                          {   'template': 'apostas_jogo.html', 
								  'titulo': 'Palpites de Todos',
								  'subtitulo': user_inscricao.competicao.campeonato.nome + ' ' + user_inscricao.competicao.nome,
	                              'user_inscricao': user_inscricao, 
	                              'apostas': apostas_jogos_competicao,
	                              'jogo': j, 
	                              'competicao': user_inscricao.competicao, 
	                              'user_participante': user_inscricao.participante,
								  # url privadas contem inscricao da competicacao
								  'nome_rancking': NOME_RANCKING,
								  'url_rancking': URL_IRANCKING + str(user_inscricao.pk)+'/',
								  'nome_tabela': NOME_TABELA,
								  'url_tabela': URL_ITABELA + str(user_inscricao.pk)+'/',
								  'nome_aposta': NOME_APOSTA,
								  'url_aposta': URL_IAPOSTA + str(user_inscricao.pk)+'/',
								  'nome_perfil_competicao': NOME_APOSTA,
								  'url_perfil_competicao': URL_IPERFIL_COMPETICAO + str(user_inscricao.pk)+'/'								  
	                           })	
"""	
	                           
@login_required
def aposta(request, competicao_pk):	
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)			
	apts = Aposta.objects.filter(inscricao=user_inscricao)
	return render_to_response('_base.html', 
	                          {   'template': 'aposta.html', 
								  'subtitulo': user_inscricao.competicao.campeonato.nome + ' ' + user_inscricao.competicao.nome,
	                              'titulo': 'Minhas Apostas',
	                              'user_participante': user_participante,
	                              'user_inscricao': user_inscricao,
	                              'competicao': competicao,
	                              'apostas': apts, 
	                              'user_inscricao': user_inscricao
	                          })

# Altera aposta, usuario alterando sua propria aposta		
@login_required
def aposta_edit(request, user_aposta_pk):
	execute_transation = 'N'
	model = Aposta.objects.get(pk=user_aposta_pk)
	mensagem = ''	
	form = ApostaForm()
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
	else:
		mensagem = 'Nao sera mais possivel alterar aposta. Jogo encontra-se em ' + model.jogo.status.descricao
		execute_transation = 'S'
	return render_to_response('_base_simple.html', 
	                          {    'template': 'aposta_edit.html', 
	                               'execute_transation': execute_transation,
	                               'aposta': model, 
	                               'form': form, 
	                               'mensagem': mensagem}, 
	                          context_instance=RequestContext(request))	                          


def perfil_competicao(request, competicao_pk, view_inscricao_pk):
	competicao = Competicao.objects.get(pk=competicao_pk)	
	user_participante = get_participante_by_user(request.user)
	user_inscricao = get_inscricao(competicao, user_participante)
	view_inscricao = Inscricao.objects.get(pk=view_inscricao_pk)
	apostas = list()
	apts_aux = Aposta.objects.filter(inscricao=view_inscricao)
	if user_inscricao.pk != view_inscricao.pk:
		for a in apts_aux:
			if (a.jogo.status.codigo == 'A') or (a.jogo.status.codigo == 'F'):
				apostas.append(a)	
	else:
		apostas = apts_aux
	return render_to_response('_base.html', 
						      {  
								'template': 'perfil.html',
								'titulo': view_inscricao.participante.apelido,
								'subtitulo': view_inscricao.competicao.campeonato.nome + ' ' + view_inscricao.competicao.nome,
								'user_participante': user_participante,
								'user_inscricao': user_participante,
								'competicao': competicao, 								
								'view_inscricao': view_inscricao,
								'apostas': apostas
							   })

"""
# ToDo...: criar um iperfil >>> def perfil(request, view_inscricao_pk, user_inscricao_pk):							   
def iperfil_competicao(request, user_inscricao_pk, view_inscricao_pk):
	user_participante = Participante()
	user_inscricao = Inscricao.objects.get(pk=user_inscricao_pk)
	view_inscricao = Inscricao.objects.get(pk=view_inscricao_pk)
	if not user_login_is_valid(request.user, user_inscricao.participante.user):
		return redirect('/')	
	if user_inscricao.pk == view_inscricao.pk:
		apts = Aposta.objects.filter(inscricao=view_inscricao)
	else:
		# ToDo nao aparece..... apostasss
		apts = []
		apts_aux = Aposta.objects.filter(inscricao=view_inscricao)
		for a in apts_aux:
			if (a.jogo.status.codigo == 'A') or (a.jogo.status.codigo == 'F'):
				apts.append(a)
	return render_to_response('_base.html', 
						      {  
								'template': 'perfil.html',
								'titulo': view_inscricao.participante.apelido,
								'subtitulo': view_inscricao.competicao.campeonato.nome + ' ' + view_inscricao.competicao.nome,
								# possivel subtitulo
	                            'user_participante': user_inscricao.participante,
	                            'user_inscricao': user_inscricao,								
								'view_inscricao': view_inscricao,
								'competicao': view_inscricao.competicao, #enviado para montar o submenu
								'apostas': apts,
							     # url publicas contem somente a competicacao
								 'nome_rancking': NOME_RANCKING,
								 'url_rancking': URL_IRANCKING + str(user_inscricao.pk)+'/',
								 'nome_tabela': NOME_TABELA,
								 'url_tabela': URL_ITABELA + str(user_inscricao.pk)+'/',
								 'nome_aposta': NOME_APOSTA,
								 'url_aposta': URL_IAPOSTA + str(user_inscricao.pk)+'/'
							   })							   
"""

@login_required
def system(request):
	campeonatos = Campeonato.objects.all()
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base.html', {'template': 'system/campeonatos.html', 'titulo': 'Campeonatos', 'subtitulo': 'Calcular e Alterar placar', 'user_participante': user_participante, 'campeonatos': campeonatos})

@login_required
def system_campeonato_calc_jogos(request, campeonato_pk):
	campeonato = Campeonato.objects.get(pk=campeonato_pk)
	user_participante = get_participante_by_user(request.user)
	return render_to_response('_base.html', {'template': 'system/campeonato_calc_jogos.html', 'titulo': 'Calcular ' + campeonato.nome, 'subtitulo': 'Placar e calculo', 'user_participante': user_participante, 'campeonato': campeonato})

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
			if j.status.codigo != 'E':
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
	
def calcular_vencedor_jogo(j):
	if j.resultado_a > j.resultado_b:
		j.vencedor = 'A'
	elif j.resultado_a < j.resultado_b:
		j.vencedor = 'B'
	else:
		j.vencedor = 'E'
	j.save()	

# calcula a aposta.
def calcula_aposta(jogo):
	# pega somente as apostas não calculadas
	apostas = Aposta.objects.filter(jogo=jogo, calculado=False)
	"""
	if apostas.count() > 0:
		competicao = apostas[0].inscricao.competicao
	i = 0
	"""
	for a in apostas:
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
		if jogo.status.codigo == 'F':
			a.calculado = True
		a.save()
		# calcula o rancking no momento da aposta (historico de colocacao)
		"""
		i = i + 1	
		if (i == apostas.count()) or (competicao != a.inscricao.competicao):
			print('Calculando >>>>>> ' + competicao.nome + ' <> ' + str(i)+' de '+ str(apostas.count()))
			calcula_rancking_historico(competicao, jogo)
			competicao = a.inscricao.competicao"""
		
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
		
#Calcula Rancking/colocacao na aposta (Histórico)
def calcula_rancking_historico(competicao, jogo):
	inscricoes = Inscricao.objects.filter(competicao=competicao).order_by('-pontos','-quantidade_acerto_placar', '-quantidade_acerto_vencedor_um_resultado_correto', '-quantidade_acerto_vencedor','-quantidade_acerto_empate_erro_placar', '-quantidade_acerto_somente_resultado_um_time')
	col = 0
	pt_anterior = 0
	qtde_ap = 0
	qtde_av = 0
	qtde_ae = 0
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

#Calcula Rancking/colocacao
def calcula_rancking(competicao):
	inscricoes = Inscricao.objects.filter(competicao=competicao).order_by('-pontos','-quantidade_acerto_placar', '-quantidade_acerto_vencedor_um_resultado_correto', '-quantidade_acerto_vencedor','-quantidade_acerto_empate_erro_placar', '-quantidade_acerto_somente_resultado_um_time')
	col = 0
	pt_anterior = 0
	qtde_ap = 0
	qtde_av = 0
	qtde_ae = 0
	for i in inscricoes:
		col = col + 1		
		if (i.pontos != pt_anterior) or (i.quantidade_acerto_placar != qtde_ap) or (i.quantidade_acerto_vencedor != qtde_av) or (i.quantidade_acerto_empate_erro_placar != qtde_ae):			
			i.colocacao = col
		else:
			i.colocacao = col-1
		i.save()
		pt_anterior = i.pontos
		qtde_ap = i.quantidade_acerto_placar
		qtde_av = i.quantidade_acerto_vencedor
		qtde_ae = i.quantidade_acerto_empate_erro_placar
