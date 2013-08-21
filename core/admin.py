from django.contrib import admin
from core.models import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import redirect

class CampeonatoAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
		try:
			system = request.GET['system']			
		except:
			return redirect('/admin/core/campeonato/')
		if system == 'S':
			return render_to_response('_base_simple.html', 
									  {    'template': 'aposta_edit.html', 
										   'execute_transation': 'S',
										   'mensagem': 'Campeonato alterado com sucesso!'})
		return redirect('/admin/core/campeonato/')
										   
class CompeticaoAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
		try:
			system = request.GET['system']			
		except:
			return redirect('/admin/core/competicao/')
		if system == 'S':
			return render_to_response('_base_simple.html', 
									  {    'template': 'aposta_edit.html', 
										   'execute_transation': 'S',
										   'mensagem': 'Competicao alterado com sucesso!'})
		return redirect('/admin/core/competicao/')

class JogoAdmin(admin.ModelAdmin):
	def response_change(self, request, obj):
		try:
			system = request.GET['system']			
		except:
			return redirect('/admin/core/jogo/')
		if system == 'S':
			return render_to_response('_base_simple.html', 
									  {    'template': 'aposta_edit.html', 
										   'execute_transation': 'S',
										   'mensagem': 'Jogo alterado com sucesso!'})
		return redirect('/admin/core/jogo/') 										   

admin.site.register(Participante)
admin.site.register(Campeonato, CampeonatoAdmin)
admin.site.register(Grupo)
admin.site.register(Jogo, JogoAdmin)
admin.site.register(Inscricao)
admin.site.register(Aposta)
admin.site.register(Time)
admin.site.register(StatusJogo)
admin.site.register(Competicao, CompeticaoAdmin)
admin.site.register(Solicitacao)
admin.site.register(Patrocinador)
admin.site.register(Local)
admin.site.register(Competicao_Patrocinadores)
admin.site.register(Pagina)
admin.site.register(PaginaPatrocinio)
