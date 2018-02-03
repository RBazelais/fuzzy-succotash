from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^process$', views.process),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^users/(?P<id>\d+)$', views.user_dash),
	url(r'^users/dashboard$', views.open_app),
	url(r'^users/add$', views.add_item),
	url(r'^users/remove$', views.remove_item),
	url(r'^/create', views.create),

	]