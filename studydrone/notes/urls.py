from django.conf.urls import patterns, url 
 
from notes import views 
 
urlpatterns = patterns('', 
    url(r'^$', views.index), 

    url(r'^my-notes/', views.my_notes),
    url(r'^upload-notes/', views.upload_notes),
    url(r'^browse-notes/', views.browse_notes),
    url(r'^search-notes/', views.search_notes),
    url(r'^search-notes-results/', views.search_notes_results),
    # url(r'^view-individual-notes/(?P<note_id>\d+)$', views.view_individual_notes),
    url(r'^view-individual-note/', views.view_individual_notes),
	
	# this is my-notes
    url(r'^view-notes/', views.view_notes),
	# this is my-groups
	url(r'^view-groups/', views.view_groups),
	
	# not sure what this is
    url(r'^rate-notes/', views.rate_notes),
    
	url(r'^my-groups/', views.my_groups),
	url(r'^messages/', views.messages),
	url(r'^create-group/', views.create_group),
	url(r'^view-individual-group/(?P<group_id>\d+)$', views.view_individual_group),
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'), 
#    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'), 

#	url(r'^$', views.index, name='index'),
) 

