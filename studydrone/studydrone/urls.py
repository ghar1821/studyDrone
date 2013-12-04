from django.conf.urls import patterns, include, url

from studydrone import views

from django.conf import settings

from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studydrone.views.home', name='home'),
    #url(r'^studydrone/', include('studydrone.foo.urls')),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^$', views.index),
    url(r'^signup/', views.signup),
    #url(r'^settings/', views.settings),
	url(r'^logout/', views.logout),
	url(r'^help/$', views.help),
	url(r'^help/knowledge-base', views.knowledge_base),
	url(r'^help/search-knowledge-base', views.search_knowledge_base),
	url(r'^help/contact-us', views.contact_us),
	
	url(r'^needs_redirect.html' , views.needs_redirect),
    url(r'^dash/', views.dash),
	
	# Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^notes/', include('notes.urls',namespace="notes")),
    url(r'^kebabs/', include('kebabs.urls',namespace="kebabs")),
    url(r'^accounts/', include('accounts.urls',namespace="accounts")),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)

