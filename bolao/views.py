from django.shortcuts import render_to_response
from django.shortcuts import redirect
from core.models import Inscricao

def home(request):
	#return render_to_response('_base.html', {'template': 'rancking.html'})
	participante = 1
	
	url = ""
	
	qtde = Inscricao.objects.filter(participante=participante).count()
	
	print(str(qtde))
	
	if qtde > 1:
		url = "/index/"+participante+"/"
	elif qtde == 1:
		inscricoes = Inscricao.objects.filter(participante=participante)[0:1].get()
		url = "/rancking/"+str(participante)+"/"+str(inscricoes.pk)+"/"
	else:
		url = "/help/"
	
	return redirect(url)
