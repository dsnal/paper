from django.conf.urls import url
from .views import DataFileView, DataFileDetailView, ModelFileView

urlpatterns = [
	url(r'^datafile/$', DataFileView.as_view(), name='datafilepost'),
	url(r'^datafile/(?P<pk>[0-9]+)$', DataFileDetailView.as_view(), name='datadetailfilepost'),
	url(r'^modelfile/$', ModelFileView.as_view(), name='modelfileupload'),

	] 