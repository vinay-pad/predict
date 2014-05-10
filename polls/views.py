import json
import logging
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
from polls.user_stats import get_user_most_tagged_places


# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
	logger.error("Loading logging form")
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
		logger.exception("Unexpected error: ", sys.exc_info()[0])
		response_data['result'] = 'failed'
		
	return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_protect
def register(request):
	userid = request.POST['user']
	access_token = request.POST['access_token']
	res = {}
	res['success'] = False
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
			user.firstname = content['first_name'] if 'first_name' in content else None
			user.lastname = content['last_name'] if 'last_name' in content else None
			user.email = content['email'] if 'email' in content else None
			user.birthday = datetime.strptime(content['birthday'], '%m/%d/%Y') if 'birthday' in content else None
			user.gender = content['gender']  if 'gender' in content else None
			user.access_token = access_token
			user.save()	
		except:
			logger.exception("Unexpected error while saving user: ", sys.exc_info()[0])
			return render(request, 'polls/error.html', {"message": "Error saving user data to database!"})
		try:
			res = store_tagged_places(user)
		except:
			logger.exception("Unexpected error while user's tagged places: ", sys.exc_info()[0])
			return render(request, 'polls/error.html', {"message": "Error getting user data from facebook!"})
	res['user'] = user.userid

	return HttpResponse(json.dumps(res), content_type="application/json")		

def get_top_tagged_places(request):
	"""
		Method to get the user's most tagged places
	"""
	userid = request.POST['userid']
	res = get_user_most_tagged_places(userid)
	
	return render(request, 'polls/most_tagged.html', {"places": res})

def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)
