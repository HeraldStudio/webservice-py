# -*- coding:utf-8 -*-

from django.db import models

class Info(models.Model):
    title = models.CharField(max_length=500)
    channel = models.CharField(max_length=200)
    time = models.DateField()
    content = models.TextField()

class Attachment(models.Model):
    info = models.ForeignKey('Info')
    title = models.CharField(max_length=500)
    link = models.URLField()