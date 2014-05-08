#check Create your models here.

import datetime
from django.utils import timezone
from django.db import models
from decimal import Decimal


# Register your models here.

class User(models.Model):
	userid = models.CharField(max_length=200, unique=True)
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	email = models.EmailField(max_length=254)
	birthday = models.DateTimeField()
	gender = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.question_text
	
class TaggedLocation(models.Model):
	city = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=30)	
	state = models.CharField(max_length=100)
	street = models.CharField(max_length=300)
	place_zip = models.CharField(max_length=10)	
	latitude = models.DecimalField(max_digits=13, decimal_places=12, default=Decimal('0.00'))
	longitude = models.DecimalField(max_digits=13, decimal_places=12, default=Decimal('0.00'))

class TaggedPlace(models.Model):
	place_id = models.CharField(max_length=200)
	name = models.CharField(max_length=500)
	location = models.ForeignKey(TaggedLocation)

class TaggedInstance(models.Model):
	user = models.ForeignKey(User)
	instance_id = models.CharField(max_length=200)
	place = models.ForeignKey(TaggedPlace)


	
	 
	
