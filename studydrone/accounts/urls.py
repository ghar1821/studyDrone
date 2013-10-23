from django.conf.urls import patterns, url 
 
from accounts import views 
 
urlpatterns = patterns('', 
	url(r'^$', views.index),
	url(r'^login/', views.login),
	
    url(r'^points-history/', views.points_history),
    url(r'^delete-account/', views.delete_account),
    url(r'^register/', views.register),
    url(r'^register-success/', views.register_success),
   
    url(r'^delete-account/$', views.delete_account),
    url(r'^delete-user/$', views.delete_user),
    url(r'^settings/$', views.edit_user),
    url(r'^settings/avatar/$', views.edit_user_picture),
    url(r'^settings/password/$', views.edit_user_password),

) 

