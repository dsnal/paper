# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser 
from rest_framework.response import Response
from rest_framework import status

from .serializers import DataFileSerializer
from .models import DataFile
from rest_framework.renderers import JSONRenderer

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




	
