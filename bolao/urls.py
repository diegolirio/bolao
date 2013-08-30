from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^bolao/', include('bolao.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),    
    # ------------------------------------------------------------------------------------------------
    # Index
    url(r'^$', 'bolao.views.index', name='index'),
    url(r'index/^$', 'bolao.views.index', name='index'),
    # Login / Logout
    url(r'^login/', "django.contrib.auth.views.login", {"template_name": "login.html"}), 
	url(r'^logout_out/', 'core.views.logout'),
    url(r'^logout/', "django.contrib.auth.views.logout_then_login", {'login_url': '/logout_out/'}),
	
	url(r'^lembrar_senha/$', 'core.views.lembrar_senha', name='lembrar_senha'),
	url(r'^redefinir_senha/(?P<user_pk>\d+)/(?P<code_new_password>\d+)/$', 'core.views.redefinir_senha', name='redefinir_senha'),
	
    # pagina Home
	url(r'^home/$', 'core.views.home', name='home'),	
	# ------------------------------------------------------------------------------------------------
	# Urls publicas e privadas cai sempre no mesmo html, a diferente eh q a privada 
	#  tera a possivel inscricao da competicao e participante logado
	# ------------------------------------------------------------------------------------------------
    # Nao Logado (publicas)
    url(r'^rancking/(?P<competicao_pk>\d+)/$', 'core.views.rancking', name='rancking'),
    url(r'^tabela/(?P<competicao_pk>\d+)/$', 'core.views.tabela', name='tabela'),
    url(r'^aposta/(?P<competicao_pk>\d+)/$', 'core.views.aposta'),
    url(r'^apostas_jogo/(?P<competicao_pk>\d+)/(?P<jogo_pk>\d+)/$', 'core.views.apostas_jogo'),
    url(r'^aposta_edit/(?P<user_aposta_pk>\d+)/$', 'core.views.aposta_edit'),
    url(r'^perfil_competicao/(?P<competicao_pk>\d+)/(?P<view_inscricao_pk>\d+)/$', 'core.views.perfil_competicao'),
	url(r'^perfil_competicao_modal/(?P<view_inscricao_pk>\d+)/$', 'core.views.perfil_competicao_modal'),
    url(r'^perfil/$', 'core.views.cadastre_se'),
    url(r'^comparar_colocacao/(?P<competicao_pk>\d+)/(?P<view_inscricao_pk>\d+)/$', 'core.views.comparar_colocacao'),
	url(r'^get_aposta_by_inscricao/(?P<inscricao_pk>\d+)/$', 'core.views.get_aposta_by_inscricao'),
	url(r'^get_inscricao_json/(?P<inscricao_pk>\d+)/$', 'core.views.get_inscricao_json'),
	url(r'^imprimir_rancking/(?P<competicao_pk>\d+)/$', 'core.views.imprimir_rancking'),
	
	url(r'^get_one_puclicidade_pagina/(?P<pagina_codigo>\w+)/(?P<competicao_pk>\d+)/$', 'core.views.get_one_puclicidade_pagina'), # JSON
    
    # Logado (privadas) >>> url fixado sempre a competicao como parametro

#    url(r'^irancking/(?P<competicao_pk>\d+)/$', 'core.views.irancking', name='irancking'),    
 #   url(r'^itabela/(?P<user_inscricao_pk>\d+)/$', 'core.views.itabela', name='itabela'),
  #  url(r'^iaposta/(?P<user_inscricao_pk>\d+)/$', 'core.views.aposta'),
   # url(r'^iapostas_jogo/(?P<user_inscricao_pk>\d+)/(?P<jogo_pk>\d+)/$', 'core.views.iapostas_jogo'),
    #url(r'^iaposta_edit/(?P<user_aposta_pk>\d+)/$', 'core.views.iaposta_edit'),
    #url(r'^iperfil_competicao/(?P<user_inscricao_pk>\d+)/(?P<view_inscricao_pk>\d+)/$', 'core.views.iperfil_competicao'),
    #url(r'^iperfil/(?P<user_inscricao_pk>\d+)/$', 'core.views.iperfil'),
    
    # ------------------------------------------------------------------------------------------------    
    # system 
    url(r'^system/$', 'core.views.system'),
    url(r'^system/campeonato_calc_jogos/(?P<campeonato_pk>\d+)/$', 'core.views.system_campeonato_calc_jogos'),
    url(r'^system/calcular_campeonato/(?P<campeonato_pk>\d+)/$', 'core.views.system_calcular_campeonato'),
	url(r'^system/jogo_edit/(?P<campeonato_pk>\d+)/(?P<jogo_pk>\d+)/$', 'core.views.system_jogo_edit'),	
	url(r'^system/novo_jogo/(?P<campeonato_pk>\d+)/$', 'core.views.system_novo_jogo'),	
	
	url(r'^system/cadastrar_participante/(?P<participante_pk>\d+)/$', 'core.views.system_cadastrar_participante'),
	url(r'^system/consultar_participante/$', 'core.views.system_consultar_participante'),
	url(r'^system/inscricoes_participante/(?P<participante_pk>\d+)/$', 'core.views.system_inscricoes_participante'),
	url(r'^system/inscrever_participante_competicao/(?P<participante_pk>\d+)/(?P<competicao_pk>\d+)/$', 'core.views.system_inscrever_participante_competicao'),
	url(r'^system/desativar_participante_competicao/(?P<inscricao_pk>\d+)/$', 'core.views.system_desativar_participante_competicao'),
	url(r'^system/ativar_participante_competicao/(?P<inscricao_pk>\d+)/$', 'core.views.system_ativar_participante_competicao'),
	
	url(r'^system/patrocinadores_por_competicao/$', 'core.views.system_patrocinadores_por_competicao'),
	url(r'^system/paginas_publicidade/(?P<competicao_pk>\d+)/$', 'core.views.system_paginas_publicidade'),
	url(r'^system/publicidade_pagina/(?P<competicao_pk>\d+)/(?P<pagina_pk>\d+)/$', 'core.views.system_publicidade_pagina'),
	url(r'^system/competicao_publicidade/(?P<competicao_pk>\d+)/$', 'core.views.system_competicao_publicidade'),
	url(r'^system/retirar_patrocinador_competicao/(?P<competicao_patrocinador_pk>\d+)/$', 'core.views.system_retirar_patrocinador_competicao'),
	url(r'^system/incluir_patrocinador_competicao/(?P<competicao_pk>\d+)/(?P<patrocinador_pk>\d+)/$', 'core.views.system_incluir_patrocinador_competicao'),
	
	url(r'^system/retirar_patrocinio_pagina/(?P<patrocinador_pagina_pk>\d+)/$', 'core.views.system_retirar_patrocinio_pagina'),
	url(r'^system/incluir_patrocinio_pagina/(?P<pagina_pk>\d+)/(?P<patrocinador_competicao_pk>\d+)/$', 'core.views.system_incluir_patrocinio_pagina'),
	
	
	url(r'^system/send_mail_all/(?P<campeonato_pk>\d+)/$', 'core.views.system_send_mail_all'),
	
	url(r'^system/novo_patrocinador_competicao/(?P<competicao_pk>\d+)/$', 'core.views.system_novo_patrocinador_competicao'),
           
    url(r'^cadastre_se/$', 'core.views.cadastre_se'),
	url(r'^cadastre_se/alterar_senha/$', 'core.views.alterar_senha'),
	#url(r'^confirm_email/[username]/(?P<codigo_confirm>\d+)/(?P<campeonato_pk>\d+)/$', 'core.views.confirm_email'),
	url(r'^confirm_email/(?P<codigo_confirm>\d{10})/$', 'core.views.confirm_email'),
	url(r'^reenvio_confirm_email/$', 'core.views.reenvio_confirm_email'),
	#url(r'^confirmado/(?P<competicao_pk>\d+)/$', 'core.views.confirmado'),
	#url(r'^lembrar_senha/$', 'core.views.lembrar_senha'),

	url(r'^photo/$', 'core.views.photo'),
	
    #url(r'^aposta_calc/(?P<campeonato>\d+)/$', 'core.views.aposta_calc'),
    
    url(r'^solicita_inscricao/(?P<competicao_pk>\d+)/$', 'core.views.solicita_inscricao'),    
    url(r'^minhas_competicoes/$', 'core.views.minhas_competicoes'),
    url(r'^solicitacoes/(?P<competicao_pk>\d+)/$', 'core.views.solicitacoes'),	
	url(r'^aceitar_solicitacao/(?P<solicitacao_pk>\d+)/$', 'core.views.aceitar_solicitacao'),
	
	url(r'^regras/$', 'core.views.regras'),
	
	url(r'^patrocinadores/(?P<competicao_pk>\d+)/$', 'core.views.patrocinadores'),
	
	url(r'^pre_cadastro/', 'core.pre_cadastro.pre_cadastro'),
	url(r'^create_users/', 'core.pre_cadastro.create_users'),
    
 )

if settings.DEBUG:
	urlpatterns += patterns('', 
	                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

