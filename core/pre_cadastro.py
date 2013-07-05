
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

# Campeonato
campeonato = Campeonato()
campeonato.nome = 'Copa do Mundo 2014'
campeonato.save()

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

# Time
#class Time(models.Model):
#	nome = models.CharField(max_length=50, unique=True)
#	def __unicode__(self):
#		return self.nome

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

# Inscricao
idiego = Inscricao()
idiego.participante = pdiego
idiego.competicao = comp









