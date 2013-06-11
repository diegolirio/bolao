from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Participante(models.Model):
	user = models.ForeignKey(User)
	apelido = models.CharField(max_length=50)	
	def __unicode__(self):
		return self.apelido
	
class Campeonato(models.Model):
	nome = models.CharField(max_length=50)	
	def __unicode__(self):
		return self.nome
		
class Competicao(models.Model):
	campeonato = models.ForeignKey(Campeonato)
	nome = models.CharField(max_length=50)	
	def __unicode__(self):
		return self.nome + " - " + self.campeonato.nome
	
class Grupo(models.Model):
	descricao = models.CharField(max_length=50)
	campeonato = models.ForeignKey(Campeonato)
	def __unicode__(self):
		return self.descricao + " - " + self.campeonato.nome	
	
class Time(models.Model):
	nome = models.CharField(max_length=50)
	def __unicode__(self):
		return self.nome
		
class StatusJogo(models.Model):
	codigo = models.CharField(max_length=1)# { F, A, E }
	descricao = models.CharField(max_length=30)	# {F:(finalizado), A: (em andamento, atualizando processo), E: (Edicao)}
	def __unicode__(self):
		return "["+self.codigo+"] " + self.descricao	
			
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
	local = models.CharField(max_length=50, blank=True)
	status = models.ForeignKey(StatusJogo) 
	def __unicode__(self):
		r_a = ""
		r_b = ""		
		if self.status.codigo != "E":
			r_a = str(self.resultado_a)
			r_b = str(self.resultado_b)	
		
		return self.time_a + " " + r_a + " X " + r_b + " " + self.time_b + " / " + str(self.data_hora) + " / Local: " + self.local

class Inscricao(models.Model):
	data = models.DateField()
	participante = models.ForeignKey(Participante)
	competicao = models.ForeignKey(Competicao)	
	colocacao = models.IntegerField(default=1)
	
	def __unicode__(self):
		return str(self.pk) + " : Participante: " + self.participante.apelido + " / "+ self.competicao.nome 
				
	def soma(self):
		t = 0
		apostas = Aposta.objects.all().filter(inscricao=self)
		for a in apostas:
			t += a.pontos
		return t

class Aposta(models.Model):
	inscricao = models.ForeignKey(Inscricao)
	jogo = models.ForeignKey(Jogo)
	resultado_a = models.IntegerField()
	resultado_b = models.IntegerField()
	pontos = models.IntegerField()
	vencedor = models.CharField(max_length=1, blank=True) # (A - B - E)
	
	def __unicode__(self):
		return self.inscricao.participante.apelido + " / " + self.jogo.time_a + " " + str(self.jogo.resultado_a) + " X " + str(self.jogo.resultado_b) + " " + self.jogo.time_b + " / " + str(self.jogo.data_hora) + " / Local: " + self.jogo.local + " / " + self.jogo.status.descricao
	
	
