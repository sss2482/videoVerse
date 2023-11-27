# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# from models.
# Create your models here.

# class Yt_Users(models.Model):

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255)
    view_count = models.IntegerField(default=0)
    time_stamp = models.TimeField(null=True, blank=True, auto_now=True)

    
class Search_click(models.Model):
    search_query = models.TextField()
    video_clicked = models.CharField(max_length=255)
    rank = models.IntegerField(null=True, blank=True)
    time_stamp = models.TimeField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.search_query

class User_Vid_Rel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255)
    bookmarked = models.BooleanField(default=False)
    liked = models.BooleanField(null=True, blank=True)
    disliked = models.BooleanField(null=True, blank=True)

