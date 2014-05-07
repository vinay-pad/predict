import httplib2
import urllib2
import json

def store_tagged_places(user):

	http_obj = httplib2.Http()	
	resp2, tagged_places = http_obj.request("https://graph.facebook.com/"+user.userid+"/tagged_places/"+"?access_token="+user.access_token, method="GET")
	tagged_places = json.loads(tagged_places)	

	return tagged_places
