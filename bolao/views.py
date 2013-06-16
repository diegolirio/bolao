from django.shortcuts import render_to_response
from django.shortcuts import redirect
from core.models import *

def index(request):
	
	print("Usuario >>>>>> " + str(request.user))
	
	if request.user.is_authenticated():
		
		# ToDo...: Utilizar a funcao...!
		participante = Participante.objects.filter(user=request.user)[0:1].get()
		
		url = ""	
		qtde = Inscricao.objects.filter(participante=participante).count()			
		if qtde == 1:
			inscricoes = Inscricao.objects.filter(participante=participante)[0:1].get()
			url = "/irancking/"+str(inscricoes.pk)+"/"
		else:
			url = "/home/"
	else:
		url = '/home/'
	return redirect(url)
