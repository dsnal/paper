# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser 
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer, JSONRenderer


from .serializers import DataFileSerializer, ModelFileSerializer
from .models import DataFile, ModelFile
import csv
import codecs
import os
from django.conf import settings
from django.http import HttpResponse




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
	parser_classes = (MultiPartParser, FormParser)
	queryset = ModelFile.objects.all()
	parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
	renderer_classes = (CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
	serializer_class = ModelFileSerializer
	all=[]

	def post(self, request, *args, **kwargs):
		all = ""
		modelfile_serializer = ModelFileSerializer(data=request.data)
		if modelfile_serializer.is_valid():
			modelfile_serializer.save()
			data = self.request.data.get('modelfile')
			reader = csv.DictReader(data, delimiter=str(u';').encode('utf-8'))
			for row in reader:
				all+= str(row)+'\n'
			return Response(all, status=status.HTTP_201_CREATED)

	def get(self, request, path, format=None):
		file_path = os.path.join(settings.MEDIA_ROOT, path)
		if os.path.exists(file_path):
			with open(file_path, 'rb' ) as fh:
				response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
				return response
		raise Http404
	

			





	
