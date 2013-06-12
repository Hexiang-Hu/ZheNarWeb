from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^user/$',views.user,name='user'),
	url(r'^place/$',views.place,name='place'),
	url(r'^event/$',views.event,name='event'),
)