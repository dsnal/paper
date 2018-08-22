# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-06 04:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelfile', models.FileField(upload_to=b'', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]