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
	code_new_password = models.CharField(max_length=100, default="0") # Codigo para redefinir senha
	descricao_identificacao = models.CharField(max_length=100, blank=True)
	def __unicode__(self):
		return self.apelido
		
class StatusJogo(models.Model):
	codigo = models.CharField(max_length=1)# { F, A, E }
	descricao = models.CharField(max_length=30, unique=True)	# {F:(finalizado), A: (em andamento, atualizando processo), E: (Edicao)}
	def __unicode__(self):
		return "["+self.codigo+"] " + self.descricao

class TipoRegra(models.Model):
	codigo = models.CharField(max_length=1)
	nome = models.CharField(max_length=50, unique=True)	
	def __unicode__(self):
		return self.nome
	
class Campeonato(models.Model):
	nome = models.CharField(max_length=50, unique=True)	
	status = models.ForeignKey(StatusJogo,default='E')
	tipo_regra = models.ForeignKey(TipoRegra)
	def __unicode__(self):
		return self.nome + ' ' + self.status.descricao
		
#23		
class Patrocinador(models.Model):
	nome_visual = models.CharField(max_length=30)	
	nome = models.CharField(max_length=50)	
	url_site = models.CharField(max_length=100)	
	# ToDo..:
	image_aside = models.ImageField(upload_to="images/patrocinadores/", blank=True) # padrao >>>>     height_field='50', width_field='100'
	#image_center = models.ImageField # padrao 200X400 analisar	
	def __unicode__(self):
		return self.nome
		
class Competicao(models.Model):
	campeonato = models.ForeignKey(Campeonato)
	nome = models.CharField(max_length=50)	
	presidente = models.ForeignKey(Participante)
	#patrocinador = models.ForeignKey(Patrocinador, blank=True, null=True)
	patrocinadores = models.ManyToManyField(Patrocinador, through='Competicao_Patrocinadores') #, blank=True,null=True)
	#patrocinadores = models.ManyToManyField(Patrocinador)
	valor_aposta = models.FloatField(default=0)
	visivel_participantes_pendente_pagamento = models.BooleanField(default=True)
	mensagem_para_pagamento_pendente = models.CharField(max_length=200, default=u'Realize seu pagamento para oficializar sua participacao no SuperBolao.com')	
	slug = models.SlugField(max_length=100, blank=True)
	def __unicode__(self):
		return self.nome + " - " + self.campeonato.nome
	class Meta:
		unique_together = ('campeonato', 'nome')
		
from django.db.models import signals
from django.template.defaultfilters import slugify

def competicao_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

signals.pre_save.connect(competicao_pre_save, sender=Competicao)		
		
class Competicao_Patrocinadores(models.Model):
	patrocinador = models.ForeignKey(Patrocinador)
	competicao = models.ForeignKey(Competicao)
	principal = models.BooleanField(default=False) # Principal Cobrar dominio 30, mais hospedagem 20 = (50)
	def __unicode__(self):
		return self.patrocinador.nome_visual + ' - Copa ' + self.competicao.nome + ' - ' + self.competicao.campeonato.nome
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
	resultado_a = models.IntegerField(default=0)
	resultado_b = models.IntegerField(default=0)
	grupo = models.ForeignKey(Grupo)
	data_hora = models.DateTimeField(default=datetime.now)
	#hora = models.CharField(max_length=15)
	vencedor = models.CharField(max_length=1, blank=True, default='E') # (A - B - E)
	local = models.ForeignKey(Local, blank=True, null=True)
	# ToDo...:
	#rodada = models.IntegerField(default=0)
	#is_by_rodada = models.BooleanField(default=False)
	status = models.ForeignKey(StatusJogo, default='E') 
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
	pagamento = models.BooleanField(default=False)
	ativo = models.BooleanField(default=True)
	
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
	# ToDo...:
	#riscado = models.BooleanField(default=False)
	def __unicode__(self):
		return self.inscricao.participante.apelido + " / " + self.jogo.time_a + " " + str(self.jogo.resultado_a) + " X " + str(self.jogo.resultado_b) + " " + self.jogo.time_b + " / " + str(self.jogo.data_hora) + " / Local: " + self.jogo.local.descricao + " / " + self.jogo.status.descricao + " - Aposta: " + str(self.resultado_a) + " X " + str(self.resultado_b) + " - Calculado: " + str(self.calculado)
	
class Solicitacao(models.Model):
	participante = models.ForeignKey(Participante)
	competicao = models.ForeignKey(Competicao)
	status = models.CharField(max_length=1, default='P') # P=Pendente | A=Aceita | R=Rejeitada
	observacao = models.CharField(max_length=150, blank=True)
	data_hora = models.DateTimeField(default=datetime.now)
	def __unicode__(self):
		return 'Solicitacao: ' + self.status + ' - ' + self.participante.apelido + ' - ' + self.competicao.nome

#23 
class Pagina(models.Model):
	# H = Home
	# T = Tabela ( 5 lateral ) R$ 6 (principal ganha 1)
 	# R = Rancking ( 5 lateral ) R$ 8 (principal ganha 1)
	# A = Aposta do Jogo | talvez minhas apostas ( 5 lateral ) R$ 5
	# I = LogIn (nenhum)
	# O = LogOut (1 lateral) R$ 3
	# F = Popup Float ( ? ? )
	# S = Solicitacao Inscricao... (2 top) R$ 1
	# C = Confirmado ( 1 lateral ) R$ 1
	nome_pagina = models.CharField(max_length=50) # Home | Tabela | Rancking ou popup_float
	codigo_pagina = models.CharField(max_length=1) # H | T | R | F
	qtde_total_patrocinio = models.IntegerField()
	valor = models.FloatField()
	def __unicode__(self):
		return self.nome_pagina
	
class PaginaPatrocinio(models.Model):
	pagina = models.ForeignKey(Pagina)
	competicacao_patrocinador = models.ForeignKey(Competicao_Patrocinadores)
	def __unicode__(self):
		return self.pagina.nome_pagina + ' - ' + self.competicacao_patrocinador.patrocinador.nome
		
		
		
