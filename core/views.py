# Create your views here.
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from core.const import *
from core.models import Participante
from core.models import Jogo
from core.models import Aposta
from core.models import Inscricao
from core.models import Competicao
from core.models import Campeonato
from core.models import Grupo

def rancking(request, inscricao):
	i = Inscricao.objects.get(pk=inscricao)
	co = i.competicao
	#participantes = Inscricao.objects.all().order_by('-pontos', 'quantidade_acerto_placar')
	#participantes = Inscricao.objects.filter(competicao=co).order_by('colocacao')
	
	inscricoes = Inscricao.objects.filter(participante=i.participante)
	inscricoes_participantes = Inscricao.objects.filter(competicao=i.competicao).order_by('colocacao')
	return render_to_response('_base.html', {'template': 'rancking.html', 'inscricoes_participantes': inscricoes_participantes, 'competicao': co, 'inscricoes': inscricoes})
	
def tabela(request, inscricao, tipo):
	i = Inscricao.objects.get(pk=inscricao)
	co = Competicao.objects.get(pk=i.competicao.pk)
	grupos = Grupo.objects.all().filter(campeonato=co.campeonato)
	jgs = []
	for g in grupos:
		js = Jogo.objects.filter(grupo=g)
		for j in js:
			jgs.append(j)
	inscricoes = Inscricao.objects.filter(participante=i.participante)
	return render_to_response('_base.html', {'template': 'tabela.html', 'jogos': jgs, 'tipo': tipo, 'competicao': co, 'inscricoes': inscricoes})	
	
def aposta(request, inscricao):
	i = Inscricao.objects.get(pk=inscricao)
	#apostas = Aposta.objects.filter(participante)
	apostas = []
	#for i in inscricoes:
	apts = Aposta.objects.filter(inscricao=i)
	for a in apts:
		apostas.append(a)
	inscricoes = Inscricao.objects.filter(participante=i.participante)
	return render_to_response('_base.html', {'template': 'aposta.html', 'apostas': apostas, 'inscricao': i, 'inscricoes': inscricoes})

def aposta_calc(request, campeonato):
	c = Campeonato.objects.get(pk=campeonato)
	grupos = Grupo.objects.filter(campeonato=c)
	for g in grupos:
		jogos = Jogo.objects.filter(grupo=g)
		for j in jogos:
			if j.resultado_a > j.resultado_b:
				j.vencedor = 'A'
			elif j.resultado_a < j.resultado_b:
				j.vencedor = 'B'
			else:
				j.vencedor = 'E'
			j.save()
			# Calcula todas as apostas de todos os participantes com este jogo
			calcula_aposta(j)
	
	competicoes = Competicao.objects.filter(campeonato=c)
	for co in competicoes:
		# Calcula pontuacao na inscricao que ingloba a soma da pontuacao
		inscricoes = Inscricao.objects.filter(competicao=co)
		for i in inscricoes:
			apostas = Aposta.objects.filter(inscricao=i)
			qtde_ap = 0
			qtde_av = 0
			qtde_ae = 0					
			pt = 0
			for a in apostas:
				pt = pt + a.pontos
				if a.pontos == PLACAR:
					qtde_ap = qtde_ap + 1	
				elif a.pontos == VENCEDOR:
					qtde_av = qtde_av + 1	
				elif a.pontos == EMPATE_SEM_PLACAR_CORRETO:
					qtde_ae = qtde_ae + 1				
			i.pontos = pt
			i.quantidade_acerto_placar = qtde_ap
			i.quantidade_acerto_vencedor = + qtde_av
			i.quantidade_acerto_empate_erro_placar = + qtde_ae
			i.save()
		#Calcula Rancking - colocacao
		calcula_rancking(co)		
	
	return redirect('/rancking/1/')

def calcula_aposta(jogo):
	apostas = Aposta.objects.filter(jogo=jogo)
	for a in apostas:
		if jogo.status.codigo != 'E':
			if (a.resultado_a == jogo.resultado_a) and (a.resultado_b == jogo.resultado_b):
				a.pontos = PLACAR
			elif (a.vencedor == jogo.vencedor) and (a.vencedor != 'E'):
				a.pontos = VENCEDOR
			elif (a.vencedor == jogo.vencedor) and (a.vencedor == 'E'):
				a.pontos = EMPATE_SEM_PLACAR_CORRETO
			else:
				a.pontos = ERRO_TUDO
		else:
			a.pontos = 0
		a.save()

def calcula_rancking(competicao):
	inscricoes = Inscricao.objects.filter(competicao=competicao).order_by('-pontos','quantidade_acerto_placar','quantidade_acerto_vencedor','quantidade_acerto_empate_erro_placar')
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
		
	#apostas = Aposta.objects.filter(inscricao.competicao = c)
#	apostas = Aposta.objects.all().order_by('-pontos', 'headline')


	
def create_jogos(request):
	"""
	cam = Campeonato()
	cam.nome = "Copa do Mundo 2014"
	cam.save()
	
	gr = Grupo()
	gr.campeonato = cam
	gr.descricao = "Grupo A"
	
	jg = Jogo()
	jg.grupo = gr
	jg.time_a = "Brasil"
	jg.time_b = "Italia"
	jg.resultado_a = 2
	jg.resultado_b = 3
	jg.data_hora = Date()
	"""
	return redirect('/tabela/1/')
	
