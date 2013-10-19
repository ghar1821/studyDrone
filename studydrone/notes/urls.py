from django.conf.urls import patterns, url 
 
from notes import views 
 
urlpatterns = patterns('', 
    url(r'^$', views.index), 

    url(r'^view-notes/', views.view_notes),
    # url(r'^view-individual-notes/(?P<note_id>\d+)$', views.view_individual_notes),
    url(r'^view-individual-note/', views.view_individual_notes),
    url(r'^upload-notes/', views.upload_notes),
    url(r'^rate-notes/', views.rate_notes),
    
	url(r'^messages/', views.messages),
    
	url(r'^view-groups/', views.view_groups),
	url(r'^view-individual-group/(?P<group_id>\d+)$', views.view_individual_group),
	url(r'^create-groups/', views.create_groups),
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'), 
#    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'), 

#	url(r'^$', views.index, name='index'),
) 

