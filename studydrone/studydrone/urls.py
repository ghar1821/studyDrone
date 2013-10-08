from django.conf.urls import patterns, include, url

from studydrone import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studydrone.views.home', name='home'),
    #url(r'^studydrone/', include('studydrone.foo.urls')),

    url(r'^$', views.index),
    url(r'^signup/', views.signup),
    url(r'^settings/', views.settings),

    url(r'^dash/', views.dash),
	
	# Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^notes/', include('notes.urls',namespace="notes")),
    url(r'^kebabs/', include('kebabs.urls',namespace="kebabs")),
    url(r'^accounts/', include('accounts.urls',namespace="accounts")),
)

