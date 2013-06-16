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
    url(r'^logout/', "django.contrib.auth.views.logout_then_login", {'login_url': '/login/'}),
    # pagina Home
	url(r'^home/$', 'core.views.home', name='home'),
	
	# ------------------------------------------------------------------------------------------------
	# Urls publicas e privadas cai sempre no mesmo html, a diferente eh q a privada 
	#  tera a possivel inscricao da competicao e participante logado
	# ------------------------------------------------------------------------------------------------
    # Nao Logado (publicas)
    url(r'^rancking/(?P<competicao_pk>\d+)/$', 'core.views.rancking', name='rancking'),
    url(r'^tabela/(?P<competicao_pk>\d+)/$', 'core.views.tabela', name='tabela'),
    url(r'^apostas_jogo/(?P<competicao_pk>\d+)/(?P<jogo_pk>\d+)/$', 'core.views.apostas_jogo'),
    url(r'^perfil/(?P<inscricao_pk>\d+)/$', 'core.views.perfil'),
    # Logado (privadas) >>> url fixado sempre a competicao como parametro
    url(r'^irancking/(?P<inscricao_pk>\d+)/$', 'core.views.irancking', name='irancking'),    
    url(r'^itabela/(?P<inscricao_pk>\d+)/$', 'core.views.itabela', name='itabela'),
    url(r'^iapostas_jogo/(?P<inscricao_pk>\d+)/(?P<jogo_pk>\d+)/$', 'core.views.iapostas_jogo'),
    url(r'^iaposta/(?P<inscricao>\d+)/$', 'core.views.aposta'),
    # ------------------------------------------------------------------------------------------------    
    url(r'^aposta_calc/(?P<campeonato>\d+)/$', 'core.views.aposta_calc'),
    url(r'^aposta_edit/(?P<pk>\d+)/$', 'core.views.aposta_edit'),
 )

if settings.DEBUG:
	urlpatterns += patterns('', 
	                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
