# -*- encoding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from core.models import *

def brasileiro():
	tipo_p = TipoRegra.objects.filter(codigo='P')[0:1].get()
	if Campeonato.objects.filter(nome='Campeonato Brasileiro 2013 - 2º Turno').count() == 0:
		campeonato = Campeonato()
		campeonato.nome = 'Campeonato Brasileiro 2013 - 2º Turno'
		campeonato.status = StatusJogo.objects.filter(codigo='E')[0:1].get()
		campeonato.tipo_regra = tipo_p
		campeonato.save()
	else:
		campeonato = Campeonato.objects.filter(nome='Campeonato Brasileiro 2013 - 2º Turno')[0:1].get()
		
	pdiego = Participante.objects.filter(apelido='Diego Lirio')[0:1].get()
		
	if Competicao.objects.filter(nome='2013', campeonato=campeonato).count() == 0:
		comp = Competicao()
		comp.campeonato = campeonato
		comp.nome = '2013'
		comp.presidente = pdiego
		comp.save()	
	else:
		comp = Competicao.objects.filter(nome='2013', campeonato=campeonato)[0:1].get()
		
	asisco = Patrocinador.objects.filter(nome_visual='Asisco')[0:1].get()
	if Competicao_Patrocinadores.objects.filter(competicao=comp, patrocinador=asisco).count() == 0:
		com_p = Competicao_Patrocinadores()
		com_p.competicao = comp
		com_p.patrocinador = asisco
		com_p.principal = True
		com_p.save()						
	# Grupo
	if Grupo.objects.filter(descricao='Série A', campeonato=campeonato).count() == 0:
		sa = Grupo()
		sa.descricao = 'Série A'
		sa.campeonato = campeonato
		sa.save()	
	else:
		sa = Grupo.objects.filter(descricao='Série A', campeonato=campeonato)[0:1].get()
	####################################################
	# Jogo
	e = StatusJogo.objects.filter(codigo='E')[0:1].get()
	if Jogo.objects.filter(time_a='Atlético-PR', time_b='Fluminense').count() == 0:
		j = Jogo()
		j.time_a = 'Atlético-PR'
		j.time_b = 'Fluminense'
		j.resultado_a = 0
		j.resultado_b = 0
		j.grupo = sa
		j.data_hora = datetime.datetime(2013, 09, 11, 19, 30, 00, 883118) #datetime.datetime.now()
		j.vencedor = 'E'
		j.local = Local.objects.get(pk=3)
		j.status = e	
		j.rodada = 20
		j.is_by_rodada = True
		j.save()
	else:
		j = Jogo.objects.filter(time_a='Atlético-PR', time_b='Fluminense')[0:1].get()
	
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