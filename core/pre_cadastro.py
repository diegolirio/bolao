# -*- encoding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from core.models import *
import datetime

def insert_auto_paginas():
	# Local Patrocinio
	if Pagina.objects.filter(codigo_pagina='R').count() == 0:		
		rancking = Pagina()
		rancking.nome_pagina = 'Rancking'
		rancking.codigo_pagina = 'R'
		rancking.qtde_total_patrocinio = 5
		rancking.valor = 7.0
		rancking.save()
	if Pagina.objects.filter(codigo_pagina='T').count() == 0:		
		tb = Pagina()
		tb.nome_pagina = 'Tabela'
		tb.codigo_pagina = 'T'
		tb.qtde_total_patrocinio = 5
		tb.valor = 6		
		tb.save()
	if Pagina.objects.filter(codigo_pagina='A').count() == 0:		
		aj = Pagina()
		aj.nome_pagina = 'Apostas do Jogo'
		aj.codigo_pagina = 'A'
		aj.qtde_total_patrocinio = 5
		aj.valor = 5		
		aj.save()
	if Pagina.objects.filter(codigo_pagina='E').count() == 0:		
		ae = Pagina()
		ae.nome_pagina = 'Alteracao resultado'
		ae.codigo_pagina = 'E'
		ae.qtde_total_patrocinio = 1
		ae.valor = 5		
		ae.save()		
	if Pagina.objects.filter(codigo_pagina='O').count() == 0:		
		lout = Pagina()
		lout.nome_pagina = 'Logout'
		lout.codigo_pagina = 'O'
		lout.qtde_total_patrocinio = 1
		lout.valor = 5		
		lout.save()
	if Pagina.objects.filter(codigo_pagina='S').count() == 0:		
		sol = Pagina()
		sol.nome_pagina = 'Solicitacao da inscricao'
		sol.codigo_pagina = 'S'
		sol.qtde_total_patrocinio = 2
		sol.valor = 2	
		sol.save()
	if Pagina.objects.filter(codigo_pagina='K').count() == 0:		
		rt = Pagina()
		rt.nome_pagina = 'Rancking Topo'
		rt.codigo_pagina = 'K'
		rt.qtde_total_patrocinio = 1
		rt.valor = 11	
		rt.save()	
	if Pagina.objects.filter(codigo_pagina='B').count() == 0:		
		tt = Pagina()
		tt.nome_pagina = 'Tabela Topo'
		tt.codigo_pagina = 'B'
		tt.qtde_total_patrocinio = 1
		tt.valor = 10	
		tt.save()	
	if Pagina.objects.filter(codigo_pagina='M').count() == 0:		
		tt = Pagina()
		tt.nome_pagina = 'Meus Palpites'
		tt.codigo_pagina = 'M'
		tt.qtde_total_patrocinio = 1
		tt.valor = 9	
		tt.save()			
	if Pagina.objects.filter(codigo_pagina='P').count() == 0:		
		tt = Pagina()
		tt.nome_pagina = 'Aposta do Jogo Topo'
		tt.codigo_pagina = 'P'
		tt.qtde_total_patrocinio = 1
		tt.valor = 9	
		tt.save()			

def __apostas_save_all__(participante, competicao):
	inscr = Inscricao.objects.filter(participante=participante, competicao=competicao)[0:1].get()
	if Aposta.objects.filter(inscricao=inscr).count() == 0:
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

def global_():
	# User
	if User.objects.filter(username='diego').count() == 0:
		diego = User.objects.create_user('diego', 'diegolirio.dl@gmail.com', 'diego')		
	else:
		diego = User.objects.filter(username='diego')[0:1].get()
	
	# Participante
	
	if Participante.objects.filter(apelido='Diego Lirio').count() == 0:
		pdiego = Participante()
		pdiego.apelido = 'Diego Lirio'
		pdiego.ddd = 11
		pdiego.telefone = 961409798
		pdiego.user = diego
		pdiego.confirm_email = True
		pdiego.confirm_send_code = 1234567890
		pdiego.foto = 'images/users/diego.jpeg'
		pdiego.save()
	else:
		pdiego = Participante.objects.filter(apelido='Diego Lirio')[0:1].get()

	# StatusJogo
	if StatusJogo.objects.filter(codigo='E').count() == 0:
		e = StatusJogo()
		e.codigo = 'E'
		e.descricao = 'Edicao'
		e.save()
	else:
		e = StatusJogo.objects.filter(codigo='E')[0:1].get()
	if StatusJogo.objects.filter(codigo='A').count() == 0:
		a = StatusJogo()
		a.codigo = 'A'
		a.descricao = 'Andamento/Bola Rolando'
		a.save()
	else:
		a = StatusJogo.objects.filter(codigo='A')[0:1].get()
	if StatusJogo.objects.filter(codigo='F').count() == 0:
		f = StatusJogo()
		f.codigo = 'F'
		f.descricao = 'Finalizado'
		f.save()
	else:
		f = StatusJogo.objects.filter(codigo='F')[0:1].get()

	#Patrocinador Asisco
	if Patrocinador.objects.filter(nome_visual='Asisco').count() == 0:
		asisco = Patrocinador()
		asisco.nome_visual = 'Asisco'
		asisco.nome = 'Alpha Sistemas e Consultoria'
		asisco.url_site = 'http://www.asisco.com.br'
		asisco.image_aside = 'images/patrocinadores/asisco.jpg'
		asisco.save()
	else:
		asisco = Patrocinador.objects.filter(nome_visual='Asisco')[0:1].get()
		
	#Patrocinador Coca-Cola
	if Patrocinador.objects.filter(nome_visual='Coca-Cola').count() == 0:
		cc = Patrocinador()
		cc.nome_visual = 'Coca-Cola'
		cc.nome = 'Coca-Cola'
		cc.url_site = 'http://www.cocacola.com.br'
		cc.image_aside = 'images/patrocinadores/cocacola.png'
		cc.save()
	else:
		cc = Patrocinador.objects.filter(nome_visual='Coca-Cola')[0:1].get()		
		
	#Patrocinador Python
	if Patrocinador.objects.filter(nome_visual='Python').count() == 0:
		py = Patrocinador()
		py.nome_visual = 'Python'
		py.nome = 'Python'
		py.url_site = 'http://python.org'
		py.image_aside = 'images/patrocinadores/python.jpg'
		py.save()
	else:
		py = Patrocinador.objects.filter(nome_visual='Python')[0:1].get()	

	insert_auto_paginas()
		
	if TipoRegra.objects.filter(codigo='M').count() == 0:
		tipo_m = TipoRegra()
		tipo_m.codigo = 'M'
		tipo_m.nome = 'Mata-a-mata'
		tipo_m.save()
	else:
		tipo_m = TipoRegra.objects.filter(codigo='M')[0:1].get()
		
	if TipoRegra.objects.filter(codigo='G').count() == 0:
		tipo_g = TipoRegra()
		tipo_g.codigo = 'G'
		tipo_g.nome = 'Grupo'
		tipo_g.save()
	else:
		tipo_g = TipoRegra.objects.filter(codigo='G')[0:1].get()

	if TipoRegra.objects.filter(codigo='P').count() == 0:
		tipo_p = TipoRegra()
		tipo_p.codigo = 'P'
		tipo_p.nome = 'Pontos corridos'
		tipo_p.save()
	else:
		tipo_p = TipoRegra.objects.filter(codigo='P')[0:1].get()			

def copa_mundo_teste():	
	tipo_m = TipoRegra.objects.filter(codigo='M')[0:1].get()
	tipo_g = TipoRegra.objects.filter(codigo='G')[0:1].get()
	tipo_p = TipoRegra.objects.filter(codigo='P')[0:1].get()	
	# Campeonato
	if Campeonato.objects.filter(nome='Copa do Mundo 2014').count() == 0:
		campeonato = Campeonato()
		campeonato.nome = 'Copa do Mundo 2014'
		campeonato.status = StatusJogo.objects.filter(codigo='E')[0:1].get()
		campeonato.tipo_regra = tipo_g
		campeonato.save()
	else:
		campeonato = Campeonato.objects.filter(nome='Copa do Mundo 2014')[0:1].get()
	###############################################
	# competicao
	pdiego = Participante.objects.filter(apelido='Diego Lirio')[0:1].get()
	asisco = Patrocinador.objects.filter(nome_visual='Asisco')[0:1].get()
	
	if Competicao.objects.filter(nome='Ferraz', campeonato=campeonato).count() == 0:
		comp = Competicao()
		comp.campeonato = campeonato
		comp.nome = 'Ferraz'
		comp.presidente = pdiego
		#comp.patrocinador = asisco
		comp.save()	
	else:
		comp = Competicao.objects.filter(nome='Ferraz', campeonato=campeonato)[0:1].get()
	
	if Competicao_Patrocinadores.objects.filter(competicao=comp, patrocinador=asisco).count() == 0:
		com_p = Competicao_Patrocinadores()
		com_p.competicao = comp
		com_p.patrocinador = asisco
		com_p.principal = True
		com_p.save()		
	
		
	# Grupo
	if Grupo.objects.filter(descricao='Grupo A', campeonato=campeonato).count() == 0:
		a = Grupo()
		a.descricao = 'Grupo A'
		a.campeonato = campeonato
		a.save()	
	else:
		a = Grupo.objects.filter(descricao='Grupo A', campeonato=campeonato)[0:1].get()
	####################################################
	# Jogo
	e = StatusJogo.objects.filter(codigo='E')[0:1].get()
	if Jogo.objects.filter(time_a='Brasil', time_b='EUA').count() == 0:
		jogo1 = Jogo()
		jogo1.time_a = 'Brasil'
		jogo1.time_b = 'EUA'
		jogo1.resultado_a = 4
		jogo1.resultado_b = 2
		jogo1.grupo = a
		jogo1.data_hora = datetime.datetime.now()
		jogo1.vencedor = 'A'
		jogo1.local = Local.objects.get(pk=3)
		jogo1.status = e	
		jogo1.save()
	else:
		Jogo.objects.filter(time_a='Brasil', time_b='EUA')[0:1].get()
	
	#####################################################
	# Inscricao
	if Inscricao.objects.filter(participante=pdiego, competicao=comp).count() == 0:
		idiego = Inscricao()
		idiego.participante = pdiego
		idiego.competicao = comp
		idiego.save()
	else:
		idiego = Inscricao.objects.filter(participante=pdiego, competicao=comp)[0:1].get()
	######################################################
	# Aposta
	__apostas_save_all__(pdiego, comp)
	

def __local__():
	rj = Local()
	rj.descricao = 'Rio de Janeiro'
	rj.save()
	br = Local()
	br.descricao = 'Brasilia'
	br.save()	
	fort = Local()
	fort.descricao = 'Fortaleza'
	fort.save()		
	bh = Local()
	bh.descricao = 'Belo Horizonte'
	bh.save()		
	re = Local()
	re.descricao = 'Recife'
	re.save()		
	salvador = Local()
	salvador.descricao = 'Salvador'
	salvador.save()			
	
def competicao_copa_confederacoes():
	
	pdiego = Participante.objects.filter(apelido='Diego Lirio')[0:1].get()
	asisco = Patrocinador.objects.filter(nome_visual='Asisco')[0:1].get()	
	cc = Patrocinador.objects.filter(nome_visual='Coca-Cola')[0:1].get()
	py = Patrocinador.objects.filter(nome_visual='Python')[0:1].get()
	e = StatusJogo.objects.filter(codigo='E')[0:1].get()
	
	# conf
	if Campeonato.objects.filter(nome='Copa das Conferederacoes').count() == 0:
		conf = Campeonato()
		conf.nome = 'Copa das Conferederacoes'
		conf.status = StatusJogo.objects.filter(codigo='E')[0:1].get()
		conf.tipo_regra = TipoRegra.objects.filter(codigo='G')[0:1].get()
		conf.save()
	else:
		conf = Campeonato.objects.filter(nome='Copa das Conferederacoes')[0:1].get()
	###############################################
	# comp_teste
	if Competicao.objects.filter(nome='Ferraz', campeonato=conf).count() == 0:
		comp_teste = Competicao()
		comp_teste.campeonato = conf
		comp_teste.nome = 'Ferraz'
		comp_teste.status = e
		comp_teste.presidente = pdiego
		#comp_teste.patrocinador = asisco
		comp_teste.valor_aposta = 10.00
		comp_teste.save()
	else:
		comp_teste = Competicao.objects.filter(nome='Ferraz', campeonato=conf)[0:1].get()
	##################################################
	# Patrocinadores
	if Competicao_Patrocinadores.objects.filter(competicao=comp_teste, patrocinador=cc).count() == 0:
		com_pa = Competicao_Patrocinadores()
		com_pa.competicao = comp_teste
		com_pa.patrocinador = cc
		com_pa.principal = True
		com_pa.save()			
	if Competicao_Patrocinadores.objects.filter(competicao=comp_teste, patrocinador=asisco).count() == 0:
		com_pa_ = Competicao_Patrocinadores()
		com_pa_.competicao = comp_teste
		com_pa_.patrocinador = asisco
		com_pa_.principal = False
		com_pa_.save()			
	if Competicao_Patrocinadores.objects.filter(competicao=comp_teste, patrocinador=py).count() == 0:
		com_pa_ = Competicao_Patrocinadores()
		com_pa_.competicao = comp_teste
		com_pa_.patrocinador = py
		com_pa_.principal = False
		com_pa_.save()			
		
		
		
	##################################################
	# Grupo_Conf
	if Grupo.objects.filter(descricao = 'Grupo A').count() == 0:
		a_ = Grupo()
		a_.descricao = 'Grupo A'
		a_.campeonato = conf
		a_.save()
	else:
		a_ = Grupo.objects.filter(descricao = 'Grupo A')[0:1].get()
	# Grupo_Conf
	if Grupo.objects.filter(descricao = 'Grupo B').count() == 0:
		b_ = Grupo()
		b_.descricao = 'Grupo B'
		b_.campeonato = conf
		b_.save()
	else:
		b_ = Grupo.objects.filter(descricao = 'Grupo B')[0:1].get()		
	# Time
	#class Time(models.Model):
	#	nome = models.CharField(max_length=50, unique=True)
	#	def __unicode__(self):
	#		return self.nome
	####################################################
	l1 = Local.objects.filter(descricao='Brasilia')[0:1].get()
	if Jogo.objects.filter(time_a='Brasil',time_b='Japao', grupo=a_, local=l1).count() == 0:
		jogo_1 = Jogo()
		jogo_1.time_a = 'Brasil'
		jogo_1.time_b = 'Japao'
		jogo_1.resultado_a = 0
		jogo_1.resultado_b = 0
		jogo_1.grupo = a_
		jogo_1.data_hora = datetime.datetime.now()
		jogo_1.vencedor = 'E'
		jogo_1.local = l1
		jogo_1.status = e
		jogo_1.save()
	####################################################
	if Jogo.objects.filter(time_a='Mexico',time_b='Italia', grupo=a_).count() == 0:
		jogo_2 = Jogo()
		jogo_2.time_a = 'Mexico'
		jogo_2.time_b = 'Italia'
		jogo_2.resultado_a = 0
		jogo_2.resultado_b = 0
		jogo_2.grupo = a_
		jogo_2.data_hora = datetime.datetime.now()
		jogo_2.vencedor = 'E'
		jogo_2.local = Local.objects.filter(descricao='Rio de Janeiro')[0:1].get()
		jogo_2.status = e
		jogo_2.save()
	####################################################
	if Jogo.objects.filter(time_a='Espanha',time_b='Uruguai', grupo=b_).count() == 0:
		jogo_3 = Jogo()
		jogo_3.time_a = 'Espanha'
		jogo_3.time_b = 'Uruguai'
		jogo_3.resultado_a = 0
		jogo_3.resultado_b = 0
		jogo_3.grupo = b_
		jogo_3.data_hora = datetime.datetime.now()
		jogo_3.vencedor = 'E'
		jogo_3.local = Local.objects.filter(descricao='Recife')[0:1].get()
		jogo_3.status = e
		jogo_3.save()
	####################################################
	if Jogo.objects.filter(time_a='Taiti',time_b='Nigeria', grupo=b_).count() == 0:
		jogo_4 = Jogo()
		jogo_4.time_a = 'Taiti'
		jogo_4.time_b = 'Nigeria'
		jogo_4.resultado_a = 0
		jogo_4.resultado_b = 0
		jogo_4.grupo = b_
		jogo_4.data_hora = datetime.datetime.now()
		jogo_4.vencedor = 'E'
		jogo_4.local = Local.objects.filter(descricao='Belo Horizonte')[0:1].get()
		jogo_4.status = e
		jogo_4.save()
	####################################################
	if Jogo.objects.filter(time_a='Brasil',time_b='Mexico', grupo=a_).count() == 0:
		jogo_5 = Jogo()
		jogo_5.time_a = 'Brasil'
		jogo_5.time_b = 'Mexico'
		jogo_5.resultado_a = 0
		jogo_5.resultado_b = 0
		jogo_5.grupo = a_
		jogo_5.data_hora = datetime.datetime.now()
		jogo_5.vencedor = 'E'
		jogo_5.local = Local.objects.filter(descricao='Fortaleza')[0:1].get()
		jogo_5.status = e
		jogo_5.save()
	####################################################
	if Jogo.objects.filter(time_a='Italia',time_b='Japao', grupo=a_).count() == 0:
		jogo_6 = Jogo()
		jogo_6.time_a = 'Italia'
		jogo_6.time_b = 'Japao'
		jogo_6.resultado_a = 0
		jogo_6.resultado_b = 0
		jogo_6.grupo = a_
		jogo_6.data_hora = datetime.datetime.now()
		jogo_6.vencedor = 'E'
		jogo_6.local = Local.objects.filter(descricao='Recife')[0:1].get()
		jogo_6.status = e
		jogo_6.save()
	####################################################
	if Jogo.objects.filter(time_a='Espanha',time_b='Taiti', grupo=b_).count() == 0:
		jogo_7 = Jogo()
		jogo_7.time_a = 'Espanha'
		jogo_7.time_b = 'Taiti'
		jogo_7.resultado_a = 0
		jogo_7.resultado_b = 0
		jogo_7.grupo = b_
		jogo_7.data_hora = datetime.datetime.now()
		jogo_7.vencedor = 'E'
		jogo_7.local = Local.objects.filter(descricao='Belo Horizonte')[0:1].get()
		jogo_7.status = e	
		jogo_7.save()
	####################################################
	if Jogo.objects.filter(time_a='Nigeria',time_b='Uruguai', grupo=b_).count() == 0:
		jogo_8 = Jogo()
		jogo_8.time_a = 'Nigeria'
		jogo_8.time_b = 'Uruguai'
		jogo_8.resultado_a = 0
		jogo_8.resultado_b = 0
		jogo_8.grupo = b_
		jogo_8.data_hora = datetime.datetime.now()
		jogo_8.vencedor = 'E'
		jogo_8.local = Local.objects.filter(descricao='Salvador')[0:1].get()
		jogo_8.status = e		
		jogo_8.save()
	####################################################
	if Jogo.objects.filter(time_a='Italia',time_b='Brasil', grupo=a_).count() == 0:
		jogo_9 = Jogo()
		jogo_9.time_a = 'Italia'
		jogo_9.time_b = 'Brasil'
		jogo_9.resultado_a = 0
		jogo_9.resultado_b = 0
		jogo_9.grupo = a_
		jogo_9.data_hora = datetime.datetime.now()
		jogo_9.vencedor = 'E'
		jogo_9.local = Local.objects.filter(descricao='Salvador')[0:1].get()
		jogo_9.status = e			
		jogo_9.save()
	####################################################
	if Jogo.objects.filter(time_a='Japao',time_b='Mexico', grupo=a_).count() == 0:
		jogo_10 = Jogo()
		jogo_10.time_a = 'Japao'
		jogo_10.time_b = 'Mexico'
		jogo_10.resultado_a = 0
		jogo_10.resultado_b = 0
		jogo_10.grupo = a_
		jogo_10.data_hora = datetime.datetime.now()
		jogo_10.vencedor = 'E'
		jogo_10.local = Local.objects.filter(descricao='Belo Horizonte')[0:1].get()
		jogo_10.status = e				
		jogo_10.save()	
	####################################################
	if Jogo.objects.filter(time_a='Nigeria',time_b='Espanha', grupo=b_).count() == 0:
		jogo_11 = Jogo()
		jogo_11.time_a = 'Nigeria'
		jogo_11.time_b = 'Espanha'
		jogo_11.resultado_a = 0
		jogo_11.resultado_b = 0
		jogo_11.grupo = b_
		jogo_11.data_hora = datetime.datetime.now()
		jogo_11.vencedor = 'E'
		jogo_11.local = Local.objects.filter(descricao='Fortaleza')[0:1].get()
		jogo_11.status = e					
		jogo_11.save()
	####################################################
	if Jogo.objects.filter(time_a='Uruguai',time_b='Taiti', grupo=b_).count() == 0:
		jogo_12 = Jogo()
		jogo_12.time_a = 'Uruguai'
		jogo_12.time_b = 'Taiti'
		jogo_12.resultado_a = 0
		jogo_12.resultado_b = 0
		jogo_12.grupo = b_
		jogo_12.data_hora = datetime.datetime.now()
		jogo_12.vencedor = 'E'
		jogo_12.local = Local.objects.filter(descricao='Recife')[0:1].get()
		jogo_12.status = e						
		jogo_12.save()
	####################################################	
	# Inscricao
	if Inscricao.objects.filter(participante=pdiego, competicao=comp_teste).count() == 0:
		idiego = Inscricao()
		idiego.participante = pdiego
		idiego.competicao = comp_teste
		idiego.save()
	else:
		idiego = Inscricao.objects.filter(participante=pdiego, competicao=comp_teste)[0:1].get()
	######################################################
	# Aposta
	__apostas_save_all__(pdiego, comp_teste)	

@login_required	
def pre_cadastro(request):
	if request.user.username == 'admin':
		global_()
		__local__()
		copa_mundo_teste()	
		competicao_copa_confederacoes()
	return redirect('/')

@login_required		
def create_users(request):
	if request.user.username == 'admin':
		usuario_cad = 'usuario'
		for i in range(1,200):
			# Salvar User
			username = usuario_cad+str(i)
			user = User.objects.create_user(username, 'diegolirio.dl@gmail.com', usuario_cad+str(i))
			# Salvar Participante
			p = Participante()
			p.user = user
			p.apelido = usuario_cad+str(i)
			p.confirm_email = True
			p.confirm_send_code = i
			p.save()
			conf = Campeonato.objects.filter(nome='Copa das Conferederacoes')[0:1].get()
			compet_ = Competicao.objects.filter(nome='Ferraz', campeonato=conf)[0:1].get()
			# Salvar Inscricao
			insc = Inscricao()
			insc.participante = p
			insc.competicao = compet_
			insc.save()
			# Salvar Apostas
			__apostas_save_all__(p, compet_)
	return redirect('/')
	
