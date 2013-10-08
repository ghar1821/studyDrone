from django.conf.urls import patterns, url 
 
from kebabs import views 
 
urlpatterns = patterns('',
	url(r'^$',views.IndexView.as_view(),name='index'),
    
	url(r'^view-menu/', views.view_menu),
	url(r'^view-individual-order/', views.view_individual_order),
	url(r'^my-orders/', views.my_orders),
	
#    url(r'^$', views.IndexView.as_view(), name='index'), 
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'), 
#    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'), 
) 

