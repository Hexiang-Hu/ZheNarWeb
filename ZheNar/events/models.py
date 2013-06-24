# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from profiles.models import Profile
from django.contrib.auth.models import User
from places.models import Place
from django.utils import timezone

class Icon(models.Model):
	name = models.CharField(unique=True,max_length=255)
	
	def __unicode__(self):
		return self.name[:-4]

# Create your models here.
class EventType(models.Model):
	#name = models.CharField(max_length = 255)
	STATUS_SET = (
	(1,"Pending"),
	(2,"Accepted"),
	(3,"Rejected"),
	)
	status = models.SmallIntegerField(default = 1,choices = STATUS_SET)
	name = models.CharField(max_length = 255,blank=False)
	icon = models.ForeignKey(Icon)

	def __unicode__(self):
		return self.name


class Event(models.Model):
	CHOICE_SET = (
	(1,_("Pending")),
	(2,_("Accepted")),
	(3,_("Rejected")),
	)
	
	status = models.SmallIntegerField(default = 1,choices = CHOICE_SET)
	name = models.CharField(max_length = 255)
	description = models.TextField(blank = True)
	holder = models.ForeignKey(Profile, related_name='event_holder_set')#
	host_organization = models.CharField(max_length = 255, null = True)
	start_time = models.DateTimeField('Time that activities started')
	end_time = models.DateTimeField('Time that activities ended')
	place = models.ForeignKey(Place)
	event_type = models.ForeignKey(EventType)
	follower = models.ManyToManyField(Profile, related_name='event_follower_set')
	address = models.CharField(max_length = 255,default = 'Not mentioned')
	pic_name = models.CharField(max_length = 255, default = 'event_default.png')
	
	def __unicode__(self):
		return self.name
	
	def follower_count(self):
		return self.follower.count()
	
	def if_event_was_expired(self):
		return self.end_time < timezone.now()

	if_event_was_expired.boolean = True
	if_event_was_expired.short_description = "Expired?"
	
	class Meta:
		ordering = ['name']
		permissions = (
			('create_map_event', 'Can create map event'),
			('modify_map_event', 'Can modify map event'),
			('remove_map_event', 'Can remove map event'),
		)
