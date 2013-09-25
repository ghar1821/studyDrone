from django.conf.urls import patterns, include, url

from studydrone import views
from studydrone.views import view_individual_note

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studydrone.views.home', name='home'),
    #url(r'^studydrone/', include('studydrone.foo.urls')),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^view-note/', 'studydrone.views.view_individual_note', name='view_individual_note'),

	# Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),

	url(r'^notes/', include('notes.urls',namespace="notes")),
	url(r'^kebabs/', include('kebabs.urls',namespace="kebabs")),
	url(r'^accounts/', include('accounts.urls',namespace="accounts")),

	url(r'^gms/', include('gms.urls',namespace="gms")),
)

