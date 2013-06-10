# Create your views here.
from django.shortcuts import render_to_response
from core.models import Participante
from core.models import Jogo
from core.models import Aposta

def rancking(request):
	participantes = Participante.objects.all()
	return render_to_response('_base.html', {'template': 'rancking.html', 'participantes': participantes})
	
def tabela(request, tipo):
	jogos = Jogo.objects.all()
	return render_to_response('_base.html', {'template': 'tabela.html', 'jogos': jogos, 'tipo': tipo})	
	
def aposta(request):
	apostas = Aposta.objects.all()
	return render_to_response('_base.html', {'template': 'aposta.html', 'apostas': apostas})
