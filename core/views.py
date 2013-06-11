# Create your views here.
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from core.models import Participante
from core.models import Jogo
from core.models import Aposta
from core.models import Inscricao

def rancking(request):
	participantes = Inscricao.objects.all()
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
	
		apostas = Aposta.objects.all().filter(jogo=j)
		for a in apostas:
			if (a.resultado_a == j.resultado_a) and (a.resultado_b == j.resultado_b):
				a.pontos = 7
			elif (a.vencedor == j.vencedor) and (a.vencedor != 'E'):
				a.pontos = 5
			elif (a.vencedor == j.vencedor) and (a.vencedor == 'E'):
				a.pontos = 4
			else:
				a.pontos = 0
			a.save()						
	
	return redirect('rancking')
