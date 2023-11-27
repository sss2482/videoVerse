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
import handler
import sql_checklogin
# import didyoumean
#session_running=False
from django.http import HttpResponse


from .models import History, Search_click, User_Vid_Rel



# def main(request):
# 	if request.user.is_authenticated:
#     	output=handler.history(request.user)
#     else:
#     	output=handler.nonHistory()
#     finalOutput={}
#     for video_id in output:
#     	individual_output=mongoSearch.searchIndividual(video_id[0])
#     	for i in individual_output:
#     		finalOutput[video_id[0]]=i
#     username='login'
#     if '0' in request.session:
#     	username=request.session['0']
#     context={"flag":username,"message":finalOutput}

#     #print( finalOutput
#     return render(request,'youtube/index.html',context)
@login_required(login_url='/login/')
def index(request):
	# output=handler.history(request.user
	# )    #print( output
	output = History.objects.filter(user = request.user)
	finalOutput={}
	for video in output:
    	#print( video_id[0]
		individual_output=mongoSearch.searchIndividual(video.video_id)
    	#print( individual_output
		for i in individual_output:
			finalOutput[video.video_id]=i

	context={"flag":request.user,"message":finalOutput}

    #print( finalOutput
	return render(request,'youtube/index2.html',context)

def logout(request):
	user_logout(request)
	return redirect('/login/')
# def logout(request):
# 	if '0' in request.session:
# 		del request.session['0']
# 		request.session.modified=True
# 	return render(request,'youtube/logout.html',{})
	# return HttpResponseRedirect("youtube/index.html/")
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
	except:
		vid_history = History.objects.create(video_id=video_id, user=request.user, view_count=1)
	vid_history.save()
	# handler.add_history(request.session['0'],video_id)
	# handler.non_signed_history(video_id)

	output={"message":relatedVideo,"current_detail":current_detail,"username":username}
	print(mongoSearch.increase_view_count(video_id))
	return render(request,'youtube/watch2.html',output)

def neo(request,neo_data):
	print( 'neodata')
	data=request.GET.get('')
	#print( neo_data
	return render(request,'youtube/neo.html',{'message':neo_data})

def checklogin(request):
	# request.session[0]=''
	form=userLogin(request.POST)
	if request.method=='POST':
		#form.save()
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			#print( username,password
			# userExistingStatus=sql(username,password)
			status=sql_checklogin.checkLogin(username,password)
			# request.session['user_id']=username
			# print( 'status',type(status)
			# print( 'session',request.session['0']
			if status!=0:
				request.session[0]=username
				session_running=True
			#print( request.session['0']
	return render(request,'youtube/status.html',{})

def thanks(request):
	form=userRegistration(request.POST)
	if request.method=='POST':
		if form.is_valid():
			first_name=form.cleaned_data['first_name']
			last_name=form.cleaned_data['last_name']
			password=form.cleaned_data['password']
			email=form.cleaned_data['email']
			#age=form.cleaned_data['age']
			#sex=form.cleaned_data['sex']
			status=handler.user_registration([first_name,last_name,'sex','age','vishal_email','password'])
			if status:
				message='thanks for registration'
				return render(request,'youtube/thanks.html',{"message":message})
			#print( first_name,last_name
			message='Already registered.Please login to continue.'
			return render(request,'youtube/thanks.html',{"message":message})

def history(request):
	username=''
	if '0' in request.session:
		output=handler.history(request.session['0'])
		finalOutput={}
		for video_id in output:
			individual_output=mongoSearch.searchIndividual(video_id[0])
			for i in individual_output:
				finalOutput[video_id[0]]=i
		username=request.session['0']
	context={"user_id":username,"message":finalOutput}
	return render(request,'youtube/history.html',context)
	#return render(request,'youtube/history',{})
    	# output=handler.history(request.session['0'])
	    # #print( output
	    # finalOutput={}
	    # for video_id in output:
	    # 	#print( video_id[0]
	    # 	individual_output=mongoSearch.searchIndividual(video_id[0])
	    # 	#print( individual_output
	    # 	for i in individual_output:
	    # 		finalOutput[video_id[0]]=i
	    # username='login'
	    # if '0' in request.session:
	    # 	username=request.session['0']
	    # context={"flag":username,"message":finalOutput}


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
	print('came')
	return HttpResponse(status=204) 
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


def sq(request, id, sq_id):
	search_query = Search_click.objects.get(id=sq_id)
	search_query.video_clicked = id
	search_query.save()
	return HttpResponse(status=204)