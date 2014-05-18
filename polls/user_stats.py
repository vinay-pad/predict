import logging
from django.db.models import Count
from polls.models import User, TaggedPlace, TaggedInstance, TaggedLocation

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_user_most_tagged_places(userid):
	"""
		Helper to get the most tagged places of a user in descending order
	"""
	res = []	
	place_ids = []
	#Get tagged instances for this user
	instances = TaggedInstance.objects.filter(user=userid)
	for instance in instances:
		place_ids.append(instance.place.place_id)
	#Get the top tagged places
	tagged_places = TaggedPlace.objects.filter(place_id__in=place_ids).annotate(num=Count('taggedinstance')).order_by('-num')[:10]

	for place in tagged_places:
		entry = {}
		logger.debug("Got place "+str(place))
		entry['name'] = place.name
		entry['id'] = place.place_id
		entry['city'] = place.location.city
		entry['street'] = place.location.street
		entry['country'] = place.location.country
		res.append(entry)
	
	return res
