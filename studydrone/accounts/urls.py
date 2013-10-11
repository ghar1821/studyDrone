from django.conf.urls import patterns, url 
 
from accounts import views 
 
urlpatterns = patterns('', 
	url(r'^$', views.index),
	url(r'^login/', views.login),
	url(r'^settings/', views.settings),
    url(r'^points-history/', views.points_history),
    url(r'^delete-account/', views.delete_account),
) 

