from django.conf.urls import patterns, url 

from reporting import views

urlpatterns = patterns('',
	url(r'^$', views.index),
)
