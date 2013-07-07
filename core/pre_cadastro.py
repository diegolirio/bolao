from core.models import *
from core.views import *

def global():
	# User
	diego = User()
	diego.username = 'diego'
	diego.email = 'diegolirio.dl@gmail.com'
	diego.password = 'diego'
	diego.first_name = 'Diego'
	diego.last_name = 'Lirio'
	diego.save()

	# Participante
	pdiego = Participante()
	diego_p = User.objects.filter(username=diego.username)[0:1].get()
	pdiego.user = diego_p
	pdiego.apelido = 'Diego Lirio'
	pdiego.ddd = 11
	pdiego.telefone = 61409798
	pdiego.confirm_email = True
	pdiego.confirm_send_code = 1234567890
	pdiego.save()

	# StatusJogo
	e = StatusJogo()
	e.codigo = 'E'
	e.descricao = 'Edição'
	e.save()
	a = StatusJogo()
	a.codigo = 'A'
	a.descricao = 'Andamento/Bola Rolando'
	a.save()
	f = StatusJogo()
	f.codigo = 'F'
	f.descricao = 'Finalizado'
	f.save()

	#Patrocinador
	asisco = Patrocinador()
	asisco.nome_visual = 'Asisco'
	asisco.nome = 'Alpha Sistemas e Consultoria'
	asisco.url_site = 'http://www.asisco.com.br'
	asisco.save()

def copa_mundo_teste():
	# Campeonato
	campeonato = Campeonato()
	campeonato.nome = 'Copa do Mundo 2014'
	campeonato.save()
	###############################################
	# competicao
	comp = Competicao()
	comp.campeonato = campeonato
	comp.nome = 'Ferraz'
	comp.status = e
	comp.presidente = pdiego
	comp.patrocinador = asisco
	comp.save()	
	# Grupo
	a = Grupo()
	a.descricao = 'Grupo A'
	a.campeonato = campeonato
	a.save()	
	####################################################
	# Jogo
	jogo1 = Jogo()
	jogo1.time_a = 'Brasil'
	jogo1.time_b = 'Italia'
	jogo1.resultado_a = 4
	jogo1.resultado_b = 2
	jogo1.grupo = a
	jogo1.data_hora = datetime.datetime.now()
	jogo1.vencedor = 'A'
	jogo1.local = 'Castelão'
	jogo1.status = e	
	#####################################################
	# Inscricao
	idiego = Inscricao()
	idiego.participante = pdiego
	idiego.competicao = comp
	######################################################
	# Aposta
	# ----- aposta = Aposta()

def __local__():
	rj = Local()
	rj = 'Rio de Janeiro'
	rj.save()
	br = Local()
	br = 'Brasília'
	br.save()	
	fort = Local()
	fort = 'Fortaleza'
	fort.save()		
	bh = Local()
	bh = 'Belo Horizonte'
	bh.save()		
	re = Local()
	re = 'Recife'
	re.save()		
	salvador = Local()
	salvador = 'Salvador'
	salvador.save()			
	
def competicao_copa_confederacoes():
	# conf
	conf = Campeonato()
	conf.nome = 'Copa das Conferederacoes'
	conf.save()
	###############################################
	# comp_teste
	comp_teste = Competicao()
	comp_teste.campeonato = campeonato
	comp_teste.nome = 'Ferraz'
	comp_teste.status = e
	comp_teste.presidente = pdiego
	comp_teste.patrocinador = asisco
	comp_teste.save()
	##################################################
	# Grupo_Conf
	a_ = Grupo()
	a_.descricao = 'Grupo A'
	a_.campeonato = conf
	a_.save()
	# Grupo_Conf
	b_ = Grupo()
	b_.descricao = 'Grupo B'
	b_.campeonato = conf
	b_.save()
	# Time
	#class Time(models.Model):
	#	nome = models.CharField(max_length=50, unique=True)
	#	def __unicode__(self):
	#		return self.nome
	####################################################
	jogo_1 = Jogo()
	jogo_1.time_a = 'Brasil'
	jogo_1.time_b = 'Japão'
	jogo_1.resultado_a = 0
	jogo_1.resultado_b = 0
	jogo_1.grupo = a_
	jogo_1.data_hora = datetime.datetime.now()
	jogo_1.vencedor = 'E'
	jogo_1.local = Local.objects.filter(descricao='Brasília')[0:1].get()
	jogo_1.status = e
	jogo_1.save()
	####################################################
	jogo_2 = Jogo()
	jogo_2.time_a = 'México'
	jogo_2.time_b = 'Iatália'
	jogo_2.resultado_a = 0
	jogo_2.resultado_b = 0
	jogo_2.grupo = a_
	jogo_2.data_hora = datetime.datetime.now()
	jogo_2.vencedor = 'E'
	jogo_2.local = Local.objects.filter(descricao='Rio de Janeiro')[0:1].get()
	jogo_2.status = e
	jogo_2.save()
	####################################################
	jogo_3 = Jogo()
	jogo_3.time_a = 'Espanha'
	jogo_3.time_b = 'Uruguai'
	jogo_3.resultado_a = 0
	jogo_3.resultado_b = 0
	jogo_3.grupo = b_
	jogo_3.data_hora = datetime.datetime.now()
	jogo_3.vencedor = 'E'
	jogo_3.local = Local.objects.filter(descricao='Recife')[0:1].get()
	jogo_3.status = e
	jogo_3.save()
	####################################################
	jogo_4 = Jogo()
	jogo_4.time_a = 'Taiti'
	jogo_4.time_b = 'Nigéria'
	jogo_4.resultado_a = 0
	jogo_4.resultado_b = 0
	jogo_4.grupo = b_
	jogo_4.data_hora = datetime.datetime.now()
	jogo_4.vencedor = 'E'
	jogo_4.local = Local.objects.filter(descricao='Belo Horizonte')[0:1].get()
	jogo_4.status = e
	jogo_4.save()
	####################################################
	jogo_5 = Jogo()
	jogo_5.time_a = 'Brasil'
	jogo_5.time_b = 'México'
	jogo_5.resultado_a = 0
	jogo_5.resultado_b = 0
	jogo_5.grupo = a_
	jogo_5.data_hora = datetime.datetime.now()
	jogo_5.vencedor = 'E'
	jogo_5.local = Local.objects.filter(descricao='Fortaleza')[0:1].get()
	jogo_5.status = e
	jogo_5.save()
	####################################################
	jogo_6 = Jogo()
	jogo_6.time_a = 'Itália'
	jogo_6.time_b = 'Japão'
	jogo_6.resultado_a = 0
	jogo_6.resultado_b = 0
	jogo_6.grupo = a_
	jogo_6.data_hora = datetime.datetime.now()
	jogo_6.vencedor = 'E'
	jogo_6.local = Local.objects.filter(descricao='Recife')[0:1].get()
	jogo_6.status = e
	jogo_6.save()
	####################################################
	jogo_7 = Jogo()
	jogo_7.time_a = 'Espanha'
	jogo_7.time_b = 'Taíti'
	jogo_7.resultado_a = 0
	jogo_7.resultado_b = 0
	jogo_7.grupo = b_
	jogo_7.data_hora = datetime.datetime.now()
	jogo_7.vencedor = 'E'
	jogo_7.local = Local.objects.filter(descricao='Belo Horizonte')[0:1].get()
	jogo_7.status = e	
	jogo_7.save()
	####################################################
	jogo_8 = Jogo()
	jogo_8.time_a = 'Nigéria'
	jogo_8.time_b = 'Uruguai'
	jogo_8.resultado_a = 0
	jogo_8.resultado_b = 0
	jogo_8.grupo = b_
	jogo_8.data_hora = datetime.datetime.now()
	jogo_8.vencedor = 'E'
	jogo_8.local = Local.objects.filter(descricao='Salvador')[0:1].get()
	jogo_8.status = e		
	jogo_8.save()
	####################################################
	jogo_9 = Jogo()
	jogo_9.time_a = 'Itália'
	jogo_9.time_b = 'Brasil'
	jogo_9.resultado_a = 0
	jogo_9.resultado_b = 0
	jogo_9.grupo = a_
	jogo_9.data_hora = datetime.datetime.now()
	jogo_9.vencedor = 'E'
	jogo_9.local = Local.objects.filter(descricao='Salvador')[0:1].get()
	jogo_9.status = e			
	jogo_9.save()
	####################################################
	jogo_10 = Jogo()
	jogo_10.time_a = 'Japão'
	jogo_10.time_b = 'México'
	jogo_10.resultado_a = 0
	jogo_10.resultado_b = 0
	jogo_10.grupo = a_
	jogo_10.data_hora = datetime.datetime.now()
	jogo_10.vencedor = 'E'
	jogo_10.local = Local.objects.filter(descricao='Belo Horizonte')[0:1].get()
	jogo_10.status = e				
	jogo_10.save()	
	####################################################
	jogo_11 = Jogo()
	jogo_11.time_a = 'Nigéria'
	jogo_11.time_b = 'Espanha'
	jogo_11.resultado_a = 0
	jogo_11.resultado_b = 0
	jogo_11.grupo = b_
	jogo_11.data_hora = datetime.datetime.now()
	jogo_11.vencedor = 'E'
	jogo_11.local = Local.objects.filter(descricao='Fortaleza')[0:1].get()
	jogo_11.status = e					
	jogo_11.save()
	####################################################
	jogo_12 = Jogo()
	jogo_12.time_a = 'Uruguai'
	jogo_12.time_b = 'Taíti'
	jogo_12.resultado_a = 0
	jogo_12.resultado_b = 0
	jogo_12.grupo = b_
	jogo_12.data_hora = datetime.datetime.now()
	jogo_12.vencedor = 'E'
	jogo_12.local = Local.objects.filter(descricao='Recife')[0:1].get()
	jogo_12.status = e						
	jogo_12.save()
	####################################################
	
	# Inscricao
	idiego = Inscricao()
	idiego.participante = pdiego
	idiego.competicao = comp_teste
	# Apostas
	__apostas_save_all__(pdiego, comp_teste)






