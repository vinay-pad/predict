#check Create your models here.

import datetime
from django.utils import timezone
from django.db import models


# Register your models here.

class User(models.Model):
	userid = models.CharField(max_length=200, primary_key=True)
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	email = models.EmailField(max_length=254)
	birthday = models.DateTimeField()
	gender = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.question_text
	
