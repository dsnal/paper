# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser 
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer, JSONRenderer


from .serializers import DataFileSerializer, ModelFileSerializer, UserSerializer
from .models import DataFile, ModelFile
import csv
import codecs
import os
import mimetypes
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from django.conf import settings
from django.http import HttpResponse
from .forms import RegistrationForm
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly





class DataFileView(APIView):

	parser_classes = (MultiPartParser, FormParser)
	def post(self, request, *args, **kwargs):
		datafile_serializer = DataFileSerializer(data=request.data)
		if datafile_serializer.is_valid():
			datafile_serializer.save()
			return Response(datafile_serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(datafile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, format=None):
		datafiles=DataFile.objects.all()
		datafiles_serializers=DataFileSerializer(datafiles, many=True)
		json_data=JSONRenderer().render(datafiles_serializers.data)
		return Response(datafiles_serializers.data)

class DataFileDetailView(APIView):
	parser_classes = (MultiPartParser, FormParser)
	def get_object(self, pk):
		try:
			return DataFile.objects.get(pk=pk)
		except DataFile.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		datafile = self.get_object(pk)
		serializer = DataFileSerializer(datafile)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		datafile = self.get_object(pk)
		serializer = DataFileSerializer(datafile, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		datafile = self.get_object(pk)
		datafile.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	def fit(self, request, pk, format=None):
		return Response(status=status.HTTP_204_NO_CONTENT)

class ModelFileView(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
	parser_classes = (MultiPartParser, FormParser)
	queryset = ModelFile.objects.all()
	parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
	renderer_classes = (CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
	serializer_class = ModelFileSerializer
	all=[]

	def post(self, request, *args, **kwargs):
		all = ""
		serializer = ModelFileSerializer(data=request.data)
		if serializer.is_valid():
			#modelfile_serializer.save(uploader=self.request.user)
			serializer.save(uploader=self.request.user)
			data = self.request.data.get('modelfile')
			reader = csv.DictReader(data, delimiter=str(u';').encode('utf-8'))
			for row in reader:
				all+= str(row)+'\n'
			return Response(all, status=status.HTTP_201_CREATED)

	def perform_create(self, serializer):
		serializer.save(uploader=self.request.user)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ModelFileList(generics.ListAPIView):
	queryset = ModelFile.objects.all()
	serializer_class = ModelFileSerializer
		
	
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def download_list(request):
	modelfile_list = ModelFile.objects.all()
	context = {'filelist' : modelfile_list}
	return render(request, 'paper1/file_list.html', context)
			
def download(request,file_name):
	file_path = settings.MEDIA_ROOT +'/'+ file_name
	file_wrapper = FileWrapper(file(file_path,'rb'))
	file_mimetype = mimetypes.guess_type(file_path)
	response = HttpResponse(file_wrapper, content_type=file_mimetype)
	response['X-Sendfile'] = file_path
	response['Content-Length'] = os.stat(file_path).st_size
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
	return response

def rc(request):
	return render(request, 'paper1/rc.html')



def registerview(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request, 'paper1/rc.html')
	else:
		form = RegistrationForm()
		args = {'form':form}
		return render(request, 'paper1/registerationform.html', args)

	
