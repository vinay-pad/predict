import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
import httplib2
import urllib2

from polls.models import User
from polls.places import store_tagged_places


def index(request):
	return render(request, 'polls/login_form.html')

def login(request):
	"""
		Method to authenticate the user and log him in.
	"""
	username = request.POST['login']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	response_data = {}
	response_data['result'] = 'failed'
	try:
		if user is not None:
			if user.is_active:
				response_data['result'] = 'success'
	except:
		response_data['result'] = 'failed'
		
	return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_protect
def register(request):
	userid = request.POST['user']
	access_token = request.POST['access_token']
	
	if  userid and access_token:
		#Now use the access token to get the user information from graph api
		http_obj = httplib2.Http()	
		try:
			resp, content = http_obj.request("https://graph.facebook.com/"+userid+"?access_token="+access_token, method="GET")
			content = json.loads(content)	
		except:
			return render(request, 'polls/error.html', {"message": "Something went wrong. Please logout and login again!"})

		#confirm userid is equal to id returned from graph api
		if userid != content['id']:
			return render(request, 'polls/error.html', {"message": "Something went wrong. Please logout and login again!"})
		try:
			user = User()
			user.userid = content['id']
			user.firstname = content['first_name']
			user.lastname = content['last_name']
			user.email = content['email']
			user.birthday = datetime.strptime(content['birthday'], '%m/%d/%Y')
			user.gender = content['gender'] 
			user.access_token = access_token
			user.save()	
		except:
			return render(request, 'polls/error.html', {"message": "Error saving user data to database!"})
		try:
			res = store_tagged_places(user)
		except:
			return render(request, 'polls/error.html', {"message": "Error getting user data from facebook!"})
		
	return render(request, 'polls/detail.html', {"user": res['success'], "access": user.userid})

def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)
