import logging
import itertools
import operator
from django.db.models import Count
from polls.models import User, TaggedPlace, TaggedInstance, TaggedLocation

# Get an instance of a logger
logger = logging.getLogger(__name__)

def most_common(L, top_n):
	"""
		helper function to find the most popular elements in a list
	"""
	# get an iterable of (item, iterable) pairs
	res = []
	SL = sorted((x, i) for i, x in enumerate(L))
	groups = itertools.groupby(SL, key=operator.itemgetter(0))
	# auxiliary function to get "quality" for an item
	def _auxfun(g):
		item, iterable = g
		count = 0
		min_index = len(L)
		for _, where in iterable:
			count += 1
			min_index = min(min_index, where)
		res.append((item, count))
		return count, -min_index
	max(groups, key=_auxfun)[0]
	sorted_lst = sorted(res, key=lambda tup: tup[1], reverse=True)[:top_n]
	
	return sorted_lst

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

	#Get the top 10 tagged places
	top_place_ids = most_common(place_ids, 10)
	import pdb; pdb.set_trace()
	for top_place in top_place_ids:
		place = TaggedPlace.objects.get(place_id=top_place[0])
		entry = {}
		logger.debug("Got place "+str(place))
		entry['name'] = place.name
		entry['id'] = place.place_id
		entry['city'] = place.location.city
		entry['street'] = place.location.street
		entry['country'] = place.location.country
		entry['num_times'] = top_place[1]
		res.append(entry)
	
	return res
