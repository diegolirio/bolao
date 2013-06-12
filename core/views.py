# Create your views here.
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from core.const import *
from core.models import Participante
from core.models import Jogo
from core.models import Aposta
from core.models import Inscricao

def rancking(request):
	participantes = Inscricao.objects.all().order_by('-pontos', 'quantidade_acerto_placar')
	return render_to_response('_base.html', {'template': 'rancking.html', 'participantes': participantes})
	
def tabela(request, tipo):
	jogos = Jogo.objects.all()
	return render_to_response('_base.html', {'template': 'tabela.html', 'jogos': jogos, 'tipo': tipo})	
	
def aposta(request):
	apostas = Aposta.objects.all()
	return render_to_response('_base.html', {'template': 'aposta.html', 'apostas': apostas})

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
		calcula_inscricao(j)
		calcula_rancking(j)
		
	return redirect('rancking')

def calcula_aposta(jogo):
	apostas = Aposta.objects.all().filter(jogo=jogo)
	for a in apostas:
		if (a.resultado_a == jogo.resultado_a) and (a.resultado_b == jogo.resultado_b):
			a.pontos = PLACAR
		elif (a.vencedor == jogo.vencedor) and (a.vencedor != 'E'):
			a.pontos = VENCEDOR
		elif (a.vencedor == jogo.vencedor) and (a.vencedor == 'E'):
			a.pontos = EMPATE_SEM_PLACAR_CORRETO
		else:
			a.pontos = ERRO_TUDO
		a.save()						
			
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
		qtde_ap = 0
		qtde_av = 0
		qtde_ae = 0					
		if a.pontos == PLACAR:
			qtde_ap = qtde_ap + 1	
		elif a.pontos == VENCEDOR:
			qtde_av = qtde_av + 1	
		elif a.pontos == EMPATE_SEM_PLACAR_CORRETO:
			qtde_ae = qtde_ae + 1	
	
		i = a.inscricao
		i.pontos = i.pontos + a.pontos
		i.quantidade_acerto_placar = i.quantidade_acerto_placar + qtde_ap
		i.quantidade_acerto_vencedor = i.quantidade_acerto_vencedor + qtde_av
		i.quantidade_acerto_empate_erro_placar = i.quantidade_acerto_empate_erro_placar + qtde_ae
		i.save()

def calcula_rancking(jogo):
	inscricoes = Inscricao.objects.all().order_by('-pontos')
	col = 0
	pt_anterior = 0
	qtde_ap = 0
	qtde_av = 0
	qtde_ae = 0
	for i in inscricoes:
		if (i.pontos != pt_anterior) or (i.quantidade_acerto_placar != qtde_ap) or (i.quantidade_acerto_vencedor != qtde_av) or (i.quantidade_acerto_empate_erro_placar != qtde_ae):
			col = col + 1		
		i.colocacao = col
		i.save()
		pt_anterior = i.pontos
		qtde_ap = i.quantidade_acerto_placar
		qtde_av = i.quantidade_acerto_vencedor
		qtde_ae = i.quantidade_acerto_empate_erro_placar
		
	#apostas = Aposta.objects.filter(inscricao.competicao = c)
#	apostas = Aposta.objects.all().order_by('-pontos', 'headline')
	
	
