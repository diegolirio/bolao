from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.mail import send_mail
from core.models import *

def index(request):	
	#print("Usuario >>>>>> " + str(request.user))	
	if request.user.is_authenticated():		
		# ToDo...: Utilizar a funcao...!
		try:
			user_participante = Participante.objects.filter(user=request.user)[0:1].get()
		except:
			if request.user.username == 'admin':
				part_admin = Participante()
				part_admin.user = request.user
				part_admin.telefone = 46758597
				part_admin.apelido = 'Administrador'
				part_admin.confirm_email = True
				part_admin.confirm_send_url = '/confirm_email/' + part_admin.user.username + '/0123456789/'
				#part_admin.foto.url = '/images/users/admin.jpg')
				part_admin.save()
				request.user.email_user('Confirmacao Cadastro de Admin', 'Usuario Adminstrador cadastrado com sucesso!', from_email=None)	
				# ------------------------- Email -----------------------------------------------
				#send_mail('Subject', 'Message.', 'from@example.com', [email@provedor.com', email_2@provedor.com'])        
				#send_mail('Conrfimacao de cadastro Ferraz Bolao', 'http://localhost:8000/confirm_email/'+part_admin.confirm_send_code+ '/?user='+str(request.user.pk), 'diegolirio.dl@gmail.com', [request.user.email])																   
				# ------------------------- fim Email -----------------------------------------------
				return redirect('/system/') # cadastrese_1
			else:
				return redirect('/cadastre_se/')				
		if request.user.username == 'admin':
			url = '/system/'								
		if user_participante.confirm_email:				
			url = ""	
			qtde = Inscricao.objects.filter(participante=user_participante).count()			
			if qtde == 1:
				user_inscricao = Inscricao.objects.filter(participante=user_participante)[0:1].get()
				url = "/rancking/"+str(user_inscricao.competicao.pk)+"/"
			else:
				url = '/home/'
		else:
			url = '/cadastre_se/'
	else:
		url = '/home/'
	return redirect(url)
