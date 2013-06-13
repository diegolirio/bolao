from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bolao.views.home', name='home'),
    # url(r'^bolao/', include('bolao.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^rancking/(?P<inscricao>\d+)/$', 'core.views.rancking', name='rancking'),    
    url(r'^tabela/(?P<inscricao>\d+)/(?P<tipo>\d+)/$', 'core.views.tabela', name='tabela'),
    url(r'^aposta/(?P<inscricao>\d+)/$', 'core.views.aposta'),
    url(r'^aposta_calc/(?P<campeonato>\d+)/$', 'core.views.aposta_calc'),
    
    url(r'^create_jogos/$', 'core.views.create_jogos'),
)

if settings.DEBUG:
	urlpatterns += patterns('', 
	                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
