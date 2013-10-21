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
	
	# not sure what this is
    url(r'^rate-notes/', views.rate_notes),
    
	url(r'^my-groups/', views.my_groups),
	url(r'^messages/', views.messages),
	url(r'^send-message/', views.send_message),
	url(r'^delete-message/', views.delete_message),
	url(r'^delete-all-messages/', views.delete_all_messages),
	url(r'^create-group/', views.create_group),
	url(r'^leave-group/', views.leave_group),
	url(r'^view-individual-group/(?P<group_id>\d+)$', views.view_individual_group),
) 

