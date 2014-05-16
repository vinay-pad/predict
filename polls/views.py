import json
import logging
import sys
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import httplib2
import urllib2

from polls.places import store_tagged_places
from polls.user_stats import get_user_most_tagged_places
from polls.dao.base_dao import save_fb_user, fetch_fb_user


# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
	logger.info("Loading login page")
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

def	home(request):
	logger.info("Loading home page")
	access_token = request.GET.get('access_token')
	userid = request.GET.get('userid')

	#Update the access token for the user in the database
	user = fetch_fb_user(userid)
	logger.debug('Got user '+str(user)+' for userid '+str(userid)+str(access_token))
	if user:
		user.access_token = access_token
		user.save()
	return render(request, 'polls/home.html')
	 
def register(request):
	userid = request.POST['user']
	access_token = request.POST['access_token']
	res = {}
	res['valid'] = False
	if  userid and access_token:
		#Now use the access token to get the user information from graph api
		http_obj = httplib2.Http()	
		try:
			logger.debug("eeRegistering user "+str(userid)+" "+str(access_token))
			resp, content = http_obj.request("https://graph.facebook.com/"+userid+"?access_token="+access_token, method="GET")
			content = json.loads(content)	
			logger.debug("Content: "+str(content))
		except:
			return render(request, 'polls/error.html', {"message": "Something went wrong. Please logout and login again!"})

		logger.debug("Checking userid")
		#confirm userid is equal to id returned from graph api
		if 'id' not in content or userid != content['id']:
			return render(request, 'polls/error.html', {"message": "Something went wrong. Please logout and login again!"})
		content['access_token'] = access_token
		logger.debug("Trying to save user")
		#try:
		res = save_fb_user(content)
		logger.debug("Saved user info succesfully"+str(res))
		#except:
			#logger.exception("Unexpected error while saving user: ", sys.exc_info()[0])
			#return HttpResponse(json.dumps(res), content_type="application/json")		

	return HttpResponse(json.dumps(res), content_type="application/json")		

def retrieve_tagged_places(request):
	userid = request.POST['user']
	access_token = request.POST['access_token']
	res = {}
	res['valid'] = False
	try:
		user = fetch_fb_user(userid)
	except:
		res['valid'] = False
		res['msg'] = 'Exception while retrieving user '+str(sys.exc_info()[0])
		logger.exception("Unexpected error while user: ", sys.exc_info()[0])
		return HttpResponse(json.dumps(res), content_type="application/json")		

	try:
		res = store_tagged_places(user)
	except:
		res['valid'] = False
		res['msg'] = 'Exception while retrieving user data '+str(sys.exc_info()[0])
		logger.exception("Unexpected error while user's tagged places: ", sys.exc_info()[0])
		return HttpResponse(json.dumps(res), content_type="application/json")		

	return HttpResponse(json.dumps(res), content_type="application/json")		

def get_top_tagged_places(request):
	"""
		Method to get the user's most tagged places
	"""
	res = {}
	userid = request.POST['user']
	try:
		res['data'] = get_user_most_tagged_places(userid)
	except:
		logger.exception("Exception while getting user top tagged places")
		res['valid'] = False	
		res['data'] = None
		return HttpResponse(json.dumps(res), content_type="application/json")		
	res['valid'] = True
	return HttpResponse(json.dumps(res), content_type="application/json")		
