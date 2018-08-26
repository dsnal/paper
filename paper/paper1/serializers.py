from rest_framework import serializers
from .models import DataFile, ModelFile
from django.contrib.auth.models import User

class DataFileSerializer(serializers.ModelSerializer):
	class Meta():
		model = DataFile
		fields = ('id','filename','timestamp','file_uuid')

class ModelFileSerializer(serializers.ModelSerializer):
	
	uploader =  serializers.ReadOnlyField(source='uploader.username')
	class Meta():
		model = ModelFile
		fields = ('id','modelfile','uploader')

class UserSerializer(serializers.ModelSerializer):
	
	modelfiles = serializers.PrimaryKeyRelatedField(many=True, queryset=ModelFile.objects.all())
	class Meta():

		model = User
		fields = ('id','username','modelfiles')


