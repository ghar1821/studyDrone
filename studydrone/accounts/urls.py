from django.conf.urls import patterns, url 
 
from accounts import views 
 
urlpatterns = patterns('', 
	url(r'^$', views.index),
	url(r'^login/', views.login),
	# url(r'^settings/', views.settings),
    url(r'^points-history/', views.points_history),
    url(r'^delete-account/', views.delete_account),
    url(r'^register/', views.register),
    url(r'^register-success/', views.register_success),
    url(r'^get/(?P<user_id>\d+)/$', views.edit_user),
    url(r'^get/(?P<user_id>\d+)/edit-password/$', views.edit_user_password),
    url(r'^get/(?P<user_id>\d+)/edit-profile-picture/$', views.edit_user_picture),

) 

