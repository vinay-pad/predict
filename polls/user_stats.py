import logging
import itertools
import operator
from datetime import datetime
import calendar	
from django.db.models import Count
from polls.models import User, TaggedPlace, TaggedInstance, TaggedLocation

import httplib2
import json
import sys

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

def get_user_top_friends(userid, access_token):

	res = {}
	res['data'] = []
	try:
		logger.debug("Getting top friends for user "+userid)
		http_obj = httplib2.Http()	
		resp2, feed = http_obj.request("https://graph.facebook.com/"+userid+"/feed/"+"?access_token="+access_token, method="GET")
		feed = json.loads(feed)	
		logger.debug("Tagged places for user "+userid)
	except:
		res['valid'] = False
		res['msg'] = 'Error getting feed for the user'+userid
		return res

	try:	
		#For each feed entry
		break_out = False
		next_entry = None
		while True:
			if next_entry:
				feed = None
				try:
					logger.debug("Getting top friends for user "+userid)
					http_obj = httplib2.Http()	
					resp2, feed = http_obj.request(next_entry, method="GET")
					feed = json.loads(feed)	
					logger.debug("Tagged places for user "+userid)
				except:
					res['valid'] = False
					res['msg'] = 'Error getting feed for the user'+userid
					return res

			for entry in feed['data']:
				if 'place' in entry:
					res['data'].append(entry)
			if 'paging' in feed:
				next_entry = feed['paging']['next'] if 'next' in feed['paging'] else None
				if next_entry:
					#Check if we have gone back one year
					unix_time = next_entry.split("until=")[1]
					if (calendar.timegm(datetime.utcnow().utctimetuple()) - int(unix_time)) > 31536000:
						break_out = True
						break	
				else:
					break_out = True
					break
			if break_out:
				break
	except:
		res['valid'] = False
		return res
						
	res['valid'] = True
	return res				

