"""
	Module to fetch user information from different sources such as FB etc.
"""
import json
import httplib2
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def fetch_user_info_from_fb(userid, access_token):
	"""
		Method to fetch user information from facebook
	"""
	try:
		http_obj = httplib2.Http()	
		logger.debug("Registering user "+str(userid)+" "+str(access_token)+"\n")
		resp, content = http_obj.request("https://graph.facebook.com/"+userid+"?access_token="+access_token, method="GET")
		content = json.loads(content)	
		logger.debug("Content: "+str(content))
	except:
		raise

	return content
