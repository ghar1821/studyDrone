from django.conf.urls import patterns, url 
 
from kebabs import views 
 
urlpatterns = patterns('',
	url(r'^$', views.index),
	url(r'^view-menu/$', views.view_menu),
	url(r'^view-cart/', views.view_cart),
	url(r'^empty-cart/', views.empty_cart),
	#url(r'^view-individual-order/$', views.view_individual_order),
	url(r'^view-individual-order/(?P<order_id>\d+)$', views.view_individual_order),
	url(r'^my-orders/', views.my_orders),
	url(r'^order-not-processed/', views.order_not_processed),
	url(r'^get-details/', views.get_details),
	url(r'^submit-order/', views.submit_order),
	url(r'^order-confirmation/$', views.order_confirmation),
	
	url(r'^add-menu-item/', views.add_menu_item),
	#url(r'^add-promotion-item/', views.add_promotion_item),
#    url(r'^$', views.IndexView.as_view(), name='index'), 
#    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'), 
#    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'), 
) 

