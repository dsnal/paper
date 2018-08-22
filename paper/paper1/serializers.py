from rest_framework import serializers
from .models import DataFile, ModelFile

class DataFileSerializer(serializers.ModelSerializer):
	class Meta():
		model = DataFile
		fields = ('id','filename','timestamp','file_uuid')

class ModelFileSerializer(serializers.ModelSerializer):
	class Meta():
		model = ModelFile
		fields = ('id','modelfile')