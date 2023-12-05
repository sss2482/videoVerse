# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from youtube.forms import initialSearch,userLogin,userRegistration
import sys
sys.path.insert(0, 'youtube\databaseCreate')
import didyoumean
import mongoSearch
import neoSearch
import json


from django.http import HttpResponse

import datetime

from .models import History, Search_click, User_Vid_Rel




@login_required(login_url='/login/')
def index(request):

	output = History.objects.filter(user = request.user)
	if len(output) == 0:
		output = History.objects.all()
	liked_videos = User_Vid_Rel.objects.filter(user=request.user, liked = True)
	finalOutput={}
	video_ids = [video.video_id for video in liked_videos]
	relatedVideos = neoSearch.related_videos(video_ids)
	for obj in relatedVideos:
		for data in obj:
			individual_output=mongoSearch.searchIndividual(obj[data]['id'])
		

		for i in individual_output:
			finalOutput[obj[data]['id']]=i

	video_ids = [video.video_id for video in output]

	relatedVideos = neoSearch.related_videos(video_ids)
	for obj in relatedVideos:
		for data in obj:
			individual_output=mongoSearch.searchIndividual(obj[data]['id'])
		
		# individual_output=mongoSearch.searchIndividual(video.video_id)
    	#print( individual_output
		for i in individual_output:
			finalOutput[obj[data]['id']]=i

	context={"flag":request.user,"message":finalOutput}

    #print( finalOutput
	return render(request,'youtube/index2.html',context)

def logout(request):
	user_logout(request)
	return redirect('/login/')

@login_required(login_url='/login/')
def submit(request):
	global search_query
	context={}
	username='login'
	user = request.user
	if request.method == "GET":
		data=request.GET.get('search_key_text','')
		search_query = Search_click.objects.create(search_query=data, user=request.user)
		search_query.save()
		correctedSuggestion=didyoumean.didyoumeanResult(data)
		flag=0
		if correctedSuggestion != data:
			flag=1
			data=correctedSuggestion
		if '0' in request.session:
			username=request.session['0']
		if data:
			context={"message":data}
			neo_data=data
			searchedOutput = mongoSearch.search(context,user)
			# searchedOutput=mongoSearch.sorted_output
			if flag==1:
				context={"username":username,"flag":correctedSuggestion,"message":searchedOutput, 'sq_id':search_query.id}
			else:
				context={"username":username,"message":searchedOutput, 'sq_id':search_query.id}
		
			length=len(searchedOutput)
			return render(request,'youtube/submit2.html',context)
	return render(request,'youtube/submit2.html',{})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			user_login(request, user) 
		return redirect('/index/')
	return render(request,'youtube/login2.html',{})

def sign_up(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		usr = User.objects.create_user(username=username, password=password, email=email)
		usr.save()
		user = authenticate(request, username=username, password=password)
		if user is not None:
			user_login(request, user)
		
	return redirect('/index/')

@login_required(login_url='/login/')
def watch(request,video_id):
	neoSearchOutput=neoSearch.search_on_click(video_id)
	relatedVideo={}
	username='login'
	for obj in neoSearchOutput:
		for data in obj:
			singleOutput=mongoSearch.searchIndividual(obj[data]['id'])
			for ii in singleOutput:
				relatedVideo[obj[data]['id']]=ii
	current_video_info=mongoSearch.searchIndividual(video_id)
	current_detail={}
	for obj in current_video_info:
		current_detail=obj

	username=request.user.username
	
	try:
		vid_history = History.objects.get(video_id=video_id, user=request.user)
		vid_history.view_count+=1
	except:
		vid_history = History.objects.create(video_id=video_id, user=request.user, view_count=1)
		mongoSearch.increase_view_count(video_id)

	vid_history.save()

	liked = 0
	disliked =0
	bookmarked = 0
	try:
		rel_obj = User_Vid_Rel.objects.filter(user = request.user, video_id= video_id)[0]
		liked = 1 if rel_obj.liked else 0
		disliked = 1 if rel_obj.disliked else 0
		bookmarked = 1 if rel_obj.bookmarked else 0
	except:
		pass
	output={"message":relatedVideo,"current_detail":current_detail,"username":username, 'liked':liked,'disliked': disliked, 'bookmarked': bookmarked}
	return render(request,'youtube/watch2.html',output)


@login_required
def history(request):
	username=''
	finalOutput = ''
	output=History.objects.filter(user=request.user)
	print(output)
	finalOutput={}
	for video in output:
		individual_output=mongoSearch.searchIndividual(video.video_id)
		
		for i in individual_output:
			finalOutput[video.video_id]=i
	username=request.user
	print(finalOutput)
	context={"user_id":username,"message":finalOutput}
	return render(request,'youtube/history2.html',context)
	
@login_required
def bookmarked_videos(request):
	username=''
	finalOutput = ''
	output=User_Vid_Rel.objects.filter(user=request.user, bookmarked=True)
	print(output)
	finalOutput={}
	for video in output:
		individual_output=mongoSearch.searchIndividual(video.video_id)
		
		for i in individual_output:
			finalOutput[video.video_id]=i
	username=request.user
	print(finalOutput)
	context={"user_id":username,"message":finalOutput,'heading': 'Bookmarked Videos'}
	return render(request,'youtube/bookmark.html',context)

def trending(request):
	username=''
	finalOutput = ''
	now=datetime.date.today() - datetime.timedelta(days=2)
	output=History.objects.filter(time_stamp__gt=now).order_by('-view_count')
	view_count = {}
	for video in output:
		if video.video_id in view_count:
			view_count[video.video_id] += video.view_count
		else:
			view_count[video.video_id] = video.view_count
	videos = dict(sorted(view_count.items(), key=lambda x:x[1], reverse=True))
	print(videos)

	print(output)
	finalOutput={}
	for video_id in videos:
		individual_output=mongoSearch.searchIndividual(video_id)
		for i in individual_output:
			finalOutput[video_id]=i
	username=request.user
	print(finalOutput)
	context={"user_id":username,"message":finalOutput, 'heading': 'Trending Videos'}
	return render(request,'youtube/bookmark.html',context)

def bookmark(request, id):
	# print('came')
	try:
		obj = User_Vid_Rel.objects.get(user=request.user, video_id=id)
		if obj.bookmarked:
			obj.bookmarked = False
		else:
			obj.bookmarked = True
	except:
		obj = User_Vid_Rel.objects.create(user=request.user, video_id=id)
		obj.bookmarked = True
	obj.save()
	
	return HttpResponse(status=204)


def like(request, id, click):
	
	try:
		obj = User_Vid_Rel.objects.filter(user=request.user, video_id=id)[0]
		if int(click) == 1:
			if obj.liked:
				obj.liked = False
				mongoSearch.decrease_like_count(id)
			else: 
				obj.liked = True
				mongoSearch.increase_like_count(id)
			if obj.disliked:
				obj.disliked = False
				mongoSearch.decrease_dislike_count(id)
			
		else:
			if obj.disliked:
				obj.disliked = False
				mongoSearch.decrease_dislike_count(id)
			else: 
				obj.disliked = True
				mongoSearch.increase_dislike_count(id)
			if obj.liked:
				obj.liked = False
				mongoSearch.decrease_like_count(id)
		

	except:
		obj = User_Vid_Rel.objects.create(user=request.user, video_id=id)
		if int(click) == 1:
			obj.liked = True
			mongoSearch.increase_like_count(id)
		else:
			obj.disliked = True
			mongoSearch.increase_dislike_count(id)
	
	obj.save()

	return HttpResponse(status=204)


def sq(request, id, sq_id):
	search_query = Search_click.objects.get(id=sq_id)
	search_query.video_clicked = id
	search_query.save()
	return HttpResponse(status=204)