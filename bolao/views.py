from django.shortcuts import render_to_response
from django.shortcuts import redirect
from core.models import *

def index(request):	
	print("Usuario >>>>>> " + str(request.user))	
	if request.user.is_authenticated():		
		# ToDo...: Utilizar a funcao...!
		try:
			user_participante = Participante.objects.filter(user=request.user)[0:1].get()
		except:
			if request.user.username == 'admin':
				return redirect('/system/') # admin
			return redirect('/cadastrese_2/'+str(request.user.pk)) # cadastrese_1
		url = ""	
		qtde = Inscricao.objects.filter(participante=user_participante).count()			
		if qtde == 1:
			user_inscricao = Inscricao.objects.filter(participante=user_participante)[0:1].get()
			url = "/irancking/"+str(user_inscricao.pk)+"/"
		else:
			url = "/home/"
	else:
		url = '/home/'
	return redirect(url)
