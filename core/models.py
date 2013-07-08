from django.db import models
from django.contrib.auth.models import User
from core.const import *
from datetime import datetime

# Create your models here.

class Participante(models.Model):
	user = models.ForeignKey(User, unique=True)
	foto = models.ImageField(upload_to="images/users/", blank=True, default="images/users/user_xxx.jpg")
	apelido = models.CharField('Apelido/Nome', max_length=30)	
	ddd = models.IntegerField(default=11, max_length=2)
	telefone = models.IntegerField(blank=True, null=True)
	confirm_email = models.BooleanField(default=False)
	confirm_send_code = models.CharField(max_length=100)
	def __unicode__(self):
		return self.apelido
	
class Campeonato(models.Model):
	nome = models.CharField(max_length=50, unique=True)	
	def __unicode__(self):
		return self.nome
		
class StatusJogo(models.Model):
	codigo = models.CharField(max_length=1)# { F, A, E }
	descricao = models.CharField(max_length=30, unique=True)	# {F:(finalizado), A: (em andamento, atualizando processo), E: (Edicao)}
	def __unicode__(self):
		return "["+self.codigo+"] " + self.descricao	
		
#23		
class Patrocinador(models.Model):
	nome_visual = models.CharField(max_length=30)	
	nome = models.CharField(max_length=50)	
	url_site = models.CharField(max_length=100)	
	# ToDo..:
	#image_aside = models.ImageField # padrao 200X200 analisar
	#image_center = models.ImageField # padrao 200X400 analisar	
		
class Competicao(models.Model):
	campeonato = models.ForeignKey(Campeonato)
	nome = models.CharField(max_length=50)	
	status = models.ForeignKey(StatusJogo,default='E')
	presidente = models.ForeignKey(Participante)
	#patrocinador = models.ForeignKey(Patrocinador, blank=True, null=True)
	patrocinadores = models.ManyToManyField(Patrocinador, through='Competicao_Patrocinadores') #, blank=True,null=True)
	#patrocinadores = models.ManyToManyField(Patrocinador)
	def __unicode__(self):
		return self.nome + " - " + self.campeonato.nome + " - " + self.status.descricao
	class Meta:
		unique_together = ('campeonato', 'nome')
		
class Competicao_Patrocinadores(models.Model):
	patrocinador = models.ForeignKey(Patrocinador)
	competicao = models.ForeignKey(Competicao)
	principal = models.BooleanField(default=False)
	class Meta:
		unique_together = ('patrocinador', 'competicao')	
	
class Grupo(models.Model):
	descricao = models.CharField(max_length=50)
	campeonato = models.ForeignKey(Campeonato)
	def __unicode__(self):
		return self.descricao + " - " + self.campeonato.nome	
	
class Time(models.Model):
	nome = models.CharField(max_length=50, unique=True)
	def __unicode__(self):
		return self.nome
		
class Local(models.Model):
	descricao = models.CharField(max_length=50)
	def __unicode__(self):
		return self.descricao
					
class Jogo(models.Model):
	#time_a = models.ForeignKey(Time)
	#time_b = models.ForeignKey(Time)
	time_a = models.CharField(max_length=50)
	time_b = models.CharField(max_length=50)
	resultado_a = models.IntegerField()
	resultado_b = models.IntegerField()
	grupo = models.ForeignKey(Grupo)
	data_hora = models.DateTimeField()
	#hora = models.CharField(max_length=15)
	vencedor = models.CharField(max_length=1, blank=True) # (A - B - E)
	local = models.ForeignKey(Local, blank=True, null=True)
	status = models.ForeignKey(StatusJogo) 
	def __unicode__(self):
		r_a = ""
		r_b = ""		
		if self.status.codigo != "E":
			r_a = str(self.resultado_a)
			r_b = str(self.resultado_b)	
		
		return self.time_a + " " + r_a + " X " + r_b + " " + self.time_b + " / " + str(self.data_hora) + " - " + self.status.descricao + " / Local: " + self.local.descricao

###########################################################

class Inscricao(models.Model):
	data = models.DateField(default=datetime.now)
	participante = models.ForeignKey(Participante)
	competicao = models.ForeignKey(Competicao)
	# Pontucao (Analisar se compensa mover para um Model)
	colocacao = models.IntegerField(default=1)
	pontos = models.IntegerField(default=0)
	quantidade_acerto_placar = models.IntegerField(default=0)
	quantidade_acerto_vencedor_um_resultado_correto = models.IntegerField(default=0)
	quantidade_acerto_vencedor = models.IntegerField(default=0)
	quantidade_acerto_empate_erro_placar = models.IntegerField(default=0)
	quantidade_acerto_somente_resultado_um_time = models.IntegerField(default=0)
	quantidade_erro = models.IntegerField(default=0)
	# end Pontucao
	
	def __unicode__(self):
		return str(self.pk) + " : Participante: " + self.participante.apelido + " / "+ self.competicao.nome 
	
	class Meta:
		unique_together = ('participante', 'competicao')
	
###########################################################
class Aposta(models.Model):
	class Meta:
		unique_together = ('inscricao', 'jogo')		
		
	inscricao = models.ForeignKey(Inscricao)
	jogo = models.ForeignKey(Jogo)
	resultado_a = models.IntegerField(default=0)
	resultado_b = models.IntegerField(default=0)
	pontos = models.IntegerField(default=0)
	vencedor = models.CharField(max_length=1, blank=True, default='E') # (A - B - E)	
	calculado = models.BooleanField(default=False)
	colocacao = models.IntegerField(default=0)
	def __unicode__(self):
		return self.inscricao.participante.apelido + " / " + self.jogo.time_a + " " + str(self.jogo.resultado_a) + " X " + str(self.jogo.resultado_b) + " " + self.jogo.time_b + " / " + str(self.jogo.data_hora) + " / Local: " + self.jogo.local.descricao + " / " + self.jogo.status.descricao + " - Aposta: " + str(self.resultado_a) + " X " + str(self.resultado_b)
	
class Solicitacao(models.Model):
	participante = models.ForeignKey(Participante)
	competicao = models.ForeignKey(Competicao)
	status = models.CharField(max_length=1, default='P') # P=Pendente | A=Aceita | R=Rejeitada
	observacao = models.CharField(max_length=150, blank=True)
	data_hora = models.DateTimeField(default=datetime.now)
	def __unicode__(self):
		return 'Solicitacao: ' + self.status + ' - ' + self.participante.apelido + ' - ' + self.competicao.nome

#23 
class PatrocinadorLocal(models.Model):
	nome_pagina = models.CharField(max_length=50) # Home | Tabela | Rancking ou popup_float
	codigo_pagina = models.CharField(max_length=50) # H | T | R | F
	




