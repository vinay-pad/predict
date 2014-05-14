import httplib2
import urllib2
import json
import logging
import sys

from polls.models import TaggedLocation, TaggedPlace, TaggedInstance

# Get an instance of a logger
logger = logging.getLogger(__name__)

def store_tagged_places(user):
	"""
		Method to retrieve all the tagged places of a user.
	"""
	res = {}
	try:
		logger.debug("Getting tagges places for user "+user.firstname+" "+user.lastname)
		http_obj = httplib2.Http()	
		resp2, tagged_places = http_obj.request("https://graph.facebook.com/"+user.userid+"/tagged_places/"+"?limit=500&access_token="+user.access_token, method="GET")
		tagged_places = json.loads(tagged_places)	
		logger.debug("Tagged places for user "+user.firstname+" :"+str(tagged_places))
	except:
		res['valid'] = False
		res['msg'] = 'Error getting tagged places for user'+user.firstname
		return res
	try:	
		#For each tagged instance create a taggedInstance, taggedPlace and taggedLocation instance
		for entry in tagged_places['data']:
			tagged_location = TaggedLocation()
			tagged_location.city = entry['place']['location']['city'] if 'city' in entry['place']['location'] else ''
			tagged_location.country = entry['place']['location']['country'] if 'country' in entry['place']['location'] else ''
			if 'latitude' in entry['place']['location']:
				tagged_location.latitude =  str(entry['place']['location']['latitude'])
			if 'longitude' in entry['place']['location']:
				tagged_location.longitude =  str(entry['place']['location']['longitude'])
			tagged_location.state = entry['place']['location']['state'] if 'state' in entry['place']['location'] else ''
			tagged_location.street = entry['place']['location']['street'] if 'street' in entry['place']['location'] else ''
			tagged_location.place_zip = entry['place']['location']['zip'] if 'zip' in entry['place']['location'] else ''
			tagged_location.save()

			tagged_place = TaggedPlace()
			tagged_place.place_id = entry['place']['id']
			tagged_place.name = entry['place']['name'] if 'name' in entry['place'] else ''
			tagged_place.location = tagged_location
			tagged_place.save()	

			tagged_instance = TaggedInstance()
			tagged_instance.instance_id = entry['id']
			tagged_instance.place = tagged_place
			tagged_instance.user = user
			tagged_instance.save()
			
			res['valid'] = True
	except KeyError:
		logger.exception("A key error occured")
	except:
		res['valid'] = False
		res['msg'] = 'Exception iterating over user results '+str(sys.exc_info()[0])
	
	return res
