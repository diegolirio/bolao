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

def rancking(request, participante, inscricao):
	i = Inscricao.objects.get(pk=inscricao)
	co = i.competicao
	#participantes = Inscricao.objects.all().order_by('-pontos', 'quantidade_acerto_placar')
	participantes = Inscricao.objects.filter(competicao=co).order_by('colocacao')
	
	p = Participante.objects.get(pk=participante)
	inscricoes = Inscricao.objects.filter(participante=p)
	return render_to_response('_base.html', {'template': 'rancking.html', 'participantes': participantes, 'competicao': co, 'inscricoes': inscricoes})
	
def tabela(request, competicao, tipo):
	co = Competicao.objects.get(pk=competicao)
	grupos = Grupo.objects.all().filter(campeonato=co.campeonato)
	jgs = []
	for g in grupos:
		js = Jogo.objects.filter(grupo=g)
		for j in js:
			jgs.append(j)
	return render_to_response('_base.html', {'template': 'tabela.html', 'jogos': jgs, 'tipo': tipo, 'competicao': co})	
	
def aposta(request, participante, competicao):
	i = Inscricao.objects.filter(participante=participante, competicao=competicao)[0:1].get()
	#apostas = Aposta.objects.filter(participante)
	apostas = []
	#for i in inscricoes:
	apts = Aposta.objects.filter(inscricao=i)
	for a in apts:
		apostas.append(a)
	return render_to_response('_base.html', {'template': 'aposta.html', 'apostas': apostas, 'inscricao': i})

def aposta_calc(request):
	#participantes = Inscricao.objects.all()	
	jogos = Jogo.objects.all()
	for j in jogos:
		if j.resultado_a > j.resultado_b:
			j.vencedor = 'A'
		elif j.resultado_a < j.resultado_b:
			j.vencedor = 'B'
		else:
			j.vencedor = 'E'
		j.save()
		
		calcula_aposta(j)
		#calcula_inscricao(j)
		calcula_rancking(j)
		
	return redirect('/rancking/1/')

def calcula_aposta(jogo):
	apostas = Aposta.objects.all().filter(jogo=jogo)
	for a in apostas:
		a.inscricao.calc()
		"""
		if (a.resultado_a == jogo.resultado_a) and (a.resultado_b == jogo.resultado_b):
			a.pontos = PLACAR
		elif (a.vencedor == jogo.vencedor) and (a.vencedor != 'E'):
			a.pontos = VENCEDOR
		elif (a.vencedor == jogo.vencedor) and (a.vencedor == 'E'):
			a.pontos = EMPATE_SEM_PLACAR_CORRETO
		else:
			a.pontos = ERRO_TUDO
		a.save()		
		"""				
			
def calcula_inscricao(jogo):
	apts = Aposta.objects.all().filter(jogo=jogo)
	for a in apts:
		i = a.inscricao
		i.pontos = 0
		i.quantidade_acerto_placar = 0
		i.quantidade_acerto_vencedor = 0
		i.quantidade_acerto_empate_erro_placar = 0
		i.save()
	
	apostas = Aposta.objects.all().filter(jogo=jogo)
	for a in apostas:
		
		print(a.inscricao.participante.apelido + " = " + str(a.pontos))
		
		qtde_ap = 0
		qtde_av = 0
		qtde_ae = 0		
					
		if a.pontos == PLACAR:
			qtde_ap = qtde_ap + 1	
		elif a.pontos == VENCEDOR:
			qtde_av = qtde_av + 1	
		elif a.pontos == EMPATE_SEM_PLACAR_CORRETO:
			qtde_ae = qtde_ae + 1	
	
		insc = a.inscricao
		insc.pontos = insc.pontos + a.pontos
		insc.quantidade_acerto_placar = insc.quantidade_acerto_placar + qtde_ap
		insc.quantidade_acerto_vencedor = insc.quantidade_acerto_vencedor + qtde_av
		insc.quantidade_acerto_empate_erro_placar = insc.quantidade_acerto_empate_erro_placar + qtde_ae
		insc.save()

def calcula_rancking(jogo):
	inscricoes = Inscricao.objects.all().order_by('-pontos')
	col = 0
	pt_anterior = 0
	qtde_ap = 0
	qtde_av = 0
	qtde_ae = 0
	for i in inscricoes:
		col = col + 1		
		if (i.pontos != pt_anterior) or (i.quantidade_acerto_placar != qtde_ap) or (i.quantidade_acerto_vencedor != qtde_av) or (i.quantidade_acerto_empate_erro_placar != qtde_ae):			
			i.colocacao = col
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
	
