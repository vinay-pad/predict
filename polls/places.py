import httplib2
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
	http_obj = httplib2.Http()	
	tagged_local_business = []
	try:
		logger.debug("Getting tagged places for user "+user.firstname+" "+user.lastname)
		resp2, tagged_places = http_obj.request("https://graph.facebook.com/"+user.userid+"/tagged_places/"+"?limit=500&access_token="+user.access_token, method="GET")
		tagged_places = json.loads(tagged_places)	
		logger.debug("Tagged places for user "+user.firstname+" :"+str(tagged_places))
	except:
		res['valid'] = False
		res['msg'] = 'Error getting tagged places for user'+user.firstname
		return res
	#Filter out non interesting places like city names etc. Only fetch Local businesses
	try:
		for entry in tagged_places['data']:
			place_id = entry['place']['id']
			#Now fetch the category for this place
			logger.debug("Getting category of places for user "+user.firstname+" "+user.lastname)
			resp3, place_details = http_obj.request("https://graph.facebook.com/"+place_id+"/"+"?access_token="+user.access_token, method="GET")
			place_details = json.loads(place_details)	
			if str(place_details['category']) == "Local business":
				for cat_list in place_details['category_list']:
					if 'city' == cat_list['name']:
						continue
				logger.debug("\n@@Removing tagged places entry for user "+user.firstname+" :"+str(place_details['category'])+"\n")
				#Remove this place from the list.
				tagged_local_business.append(entry)
	except:
		res['valid'] = False
		res['msg'] = 'Error getting categories of tagged places for user'+user.firstname
		return res
		
	
	try:	
		#For each tagged instance create a taggedInstance, taggedPlace and taggedLocation instance
		for entry in tagged_local_business:
			latitude = str(entry['place']['location']['latitude']) if 'latitude' in entry['place']['location'] else None
			longitude = str(entry['place']['location']['longitude']) if 'longitude' in entry['place']['location'] else None
			try:
				tagged_location = TaggedLocation.objects.get(latitude=latitude, longitude=longitude)
			except TaggedLocation.DoesNotExist:
				tagged_location = TaggedLocation()
				tagged_location.city = entry['place']['location']['city'] if 'city' in entry['place']['location'] else ''
				tagged_location.country = entry['place']['location']['country'] if 'country' in entry['place']['location'] else ''
				if latitude:
					tagged_location.latitude =  latitude
				if longitude:
					tagged_location.longitude =  longitude
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
