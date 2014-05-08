import httplib2
import urllib2
import json

from polls.models import TaggedLocation, TaggedPlace, TaggedInstance

def store_tagged_places(user):
	
	res = {}
	http_obj = httplib2.Http()	
	resp2, tagged_places = http_obj.request("https://graph.facebook.com/"+user.userid+"/tagged_places/"+"?access_token="+user.access_token, method="GET")
	tagged_places = json.loads(tagged_places)	
	
	#For each tagged instance create a taggedInstance, taggedPlace and taggedLocation instance
	for entry in tagged_places['data']:
		tagged_location = TaggedLocation()
		tagged_location.city = entry['place']['city'] if 'city' in entry['place'] else ''
		tagged_location.country = entry['place']['country'] if 'country' in entry['place'] else ''
		if 'latitude' in entry['place']:
			tagged_location.latitude =  entry['place']['latitude']
		if 'longitude' in entry['place']:
			tagged_location.longitude =  entry['place']['longitude']
		tagged_location.state = entry['place']['state'] if 'state' in entry['place'] else ''
		tagged_location.street = entry['place']['street'] if 'street' in entry['place'] else ''
		tagged_location.place_zip = entry['place']['zip'] if 'zip' in entry['place'] else ''
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
		
		res['success'] = True
	
	return res
