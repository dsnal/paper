from django.conf.urls import url
from .views import DataFileView, DataFileDetailView, ModelFileView, ModelFileList
from . import views
from django.conf.urls import include

urlpatterns = [
	url(r'^datafile/$', DataFileView.as_view(), name='datafilepost'),
	url(r'^datafile/(?P<pk>[0-9]+)$', DataFileDetailView.as_view(), name='datadetailfilepost'),

	url(r'^modelfile/$', ModelFileView.as_view(), name='modelfileupload'),
	url(r'^modelfilelistapi/$',ModelFileList.as_view(), name='modelfilelistapi'),
	url(r'^modelfilelist/$',views.download_list, name='modelfilelist'),
	url(r'^download/(?P<file_name>.+)$', views.download, name='download'),

	url(r'^register/$', views.registerview, name='register'),
	url(r'^rc/$', views.rc, name='rc'),
	url(r'^users/$', views.UserList.as_view()),

	]
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]