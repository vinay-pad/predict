from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
import json

from polls.models import Question


def is_authenticated(caller):
	def check_user_authenticated(request):
		if not request.user.is_authenticated():
			return HttpResponseRedirect("index/")
		caller(request)
	return check_user_authenticated
		
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
	if user is not None:
		if user.is_active:
			response_data['result'] = 'success'
	return HttpResponse(json.dumps(response_data), content_type="application/json")

@is_authenticated
def detail(request, question_id):
	return HttpResponse("Not authenticated")

def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)
