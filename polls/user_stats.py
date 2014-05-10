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
	tagged_places = TaggedPlace.objects.annotate(num=Count('taggedinstance'))
	tagged_places = sorted(tagged_places, key=lambda k:k.num, reverse=True)

	for place in tagged_places:
		logger.debug("Got place\n", place)
		res.append((place.name, place.place_id))
	
	return res
