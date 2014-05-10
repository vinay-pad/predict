#check Create your models here.

import datetime
from django.utils import timezone
from django.db import models
from decimal import Decimal


# Register your models here.

class User(models.Model):
	userid = models.CharField(max_length=200, primary_key=True)
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	email = models.EmailField(max_length=254)
	birthday = models.DateTimeField(null=True)
	gender = models.CharField(max_length=20)
	access_token = models.TextField()	
	
	def __unicode__(self):
		return self.firstname+" "+self.lastname
	
class TaggedLocation(models.Model):
	city = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=30)	
	state = models.CharField(max_length=100)
	street = models.CharField(max_length=300)
	place_zip = models.CharField(max_length=10)	
	latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
	longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
	
	def __unicode__(self):
		return self.city+" "+self.state+" lat: "+str(self.latitude)+" long: "+str(self.longitude)

class TaggedPlace(models.Model):
	place_id = models.CharField(max_length=200, primary_key=True)
	name = models.CharField(max_length=500)
	location = models.ForeignKey(TaggedLocation)

	def __unicode__(self):
		return self.name

class TaggedInstance(models.Model):
	user = models.ForeignKey(User)
	instance_id = models.CharField(max_length=200, primary_key=True)
	place = models.ForeignKey(TaggedPlace)
	
	def __unicode__(self):
		return self.place.name


	
	 
	
