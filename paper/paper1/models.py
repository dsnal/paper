# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
from uuid import UUID
from json import JSONEncoder
from django.core.validators import FileExtensionValidator


class DataFile(models.Model):
	
	
	filename = models.CharField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
	file_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

class ModelFile(models.Model):
	modelfile = models.FileField(blank=False, null=False, validators=[FileExtensionValidator(allowed_extensions=['csv'])])
	timestamp = models.DateTimeField(auto_now_add=True)
