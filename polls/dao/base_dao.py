import logging
import sys
from polls.models import User
from polls.models import FBLocation
from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

def update_fb_user_location(loc_info):
	res = {}
	loc = None
	#If no location information available then return None
	
	if not loc_info:
		return None
	try:
		loc = FBLocation()
		loc.loc_id = loc_info['id'] 
		loc.name = ''
		loc.talking_about_count = 0
		loc.category = 'test'
		loc.num_checkins = 0
		loc.category_list = ['test1']
		loc.description = ''
		loc.fb_page_link = ''
		loc.website = ''
		loc.were_here_count = 0
		#Fetch the remaining location information in an asynchronous way. Otherwise the user would have
		#to wait forever if its a synchronous call.
		loc.save()
	except:
		logger.exception("Unexpected error while getting user's location: "+str(sys.exc_info()[0]))
		return None

	return loc	

def save_fb_user(content):
	"""
		Internal dao method to save/update an fb user
	"""
	res = {}
	res['valid'] = False
	try:
		user = User()
		user.userid = content['id']
		user.firstname = content['first_name'] if 'first_name' in content else None
		user.lastname = content['last_name'] if 'last_name' in content else None
		user.email = content['email'] if 'email' in content else None
		user.birthday = datetime.strptime(content['birthday'], '%m/%d/%Y') if 'birthday' in content else None
		user.gender = content['gender']  if 'gender' in content else None
		user.access_token = content['access_token']
		user.location = update_fb_user_location(content['location']) if 'location' in content else None
		user.save()	
		res['valid'] = True
		res['userid'] = content['id']
		res['access_token'] = content['access_token']
	except:
		logger.exception("Unexpected error while saving user: "+str(sys.exc_info()[0]))
		res['valid'] = False
		return res
	return res


def fetch_fb_user(userid):
	try:
		user = User.objects.filter(userid=userid)[0]
	except IndexError:
		raise
	except:
		logger.exception("Error fetching user information\n")
		return None

	return user
