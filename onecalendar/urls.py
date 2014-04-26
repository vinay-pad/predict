
from django.conf.urls import patterns, url

from onecalendar import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
)
