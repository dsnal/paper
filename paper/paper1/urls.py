from django.conf.urls import url
from .views import DataFileView, DataFileDetailView

urlpatterns = [
	url(r'^datafile/$', DataFileView.as_view(), name='datafilepost'),
	url(r'^datafile/(?P<pk>[0-9]+)$', DataFileDetailView.as_view(), name='datafilepost'),

	]