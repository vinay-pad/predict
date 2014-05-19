from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^index', views.index, name='index'),
	url(r'^login', views.login, name='login'),
	url(r'^register', views.register, name='register'),
	url(r'^get_top_tagged', views.get_top_tagged_places, name='get_top_tagged_places'),
	url(r'^home', views.home, name='homepage'),
	url(r'^retrieve_tagged_places', views.retrieve_tagged_places, name='retreive_top_tagged'),
	url(r'^fetch_top_friends', views.fetch_top_friends, name='fetch_top_friends'),
)
