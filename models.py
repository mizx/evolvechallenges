import config

from datetime import datetime
import time

from google.appengine.ext import ndb
from django.template.defaultfilters import slugify

class News(ndb.Model):
	title = ndb.StringProperty()
	subtitle = ndb.StringProperty()
	button_text = ndb.StringProperty()
	button_link = ndb.StringProperty()

class Challenge(ndb.Model):
	id = ndb.IntegerProperty(required=True)
	slug = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	
	start = ndb.DateTimeProperty(required=True)
	end = ndb.DateTimeProperty()
	checked = ndb.DateTimeProperty(auto_now=True)
	updated = ndb.DateTimeProperty()
	type = ndb.StringProperty(choices=['counter', 'versus', 'joint'], default='counter')
	
	action = ndb.StringProperty(default='')
	reward = ndb.StringProperty(default='')
	reward_stretch = ndb.StringProperty(default='')
	background = ndb.StringProperty(default='goliath_bg.jpg')
	news_url = ndb.StringProperty(default='')
	
	progress = ndb.IntegerProperty(default=0)
	goal = ndb.IntegerProperty(required=True)
	goal_stretch = ndb.IntegerProperty()
	is_stretch = ndb.BooleanProperty(default=False)
	is_active = ndb.ComputedProperty(
		lambda self: (datetime.utcnow() < self.end + config.DEFAULT_CHALLENGE_POST_DELAY and datetime.utcnow() > self.start)
	)
	is_achieved = ndb.ComputedProperty(lambda self: self.progress > self.goal)
	
	axis_y_min = ndb.IntegerProperty()
	axis_y_max = ndb.IntegerProperty()
	axis_y_label = ndb.StringProperty()

class ChallengeData(ndb.Model):
	challenge = ndb.KeyProperty(kind=Challenge)
	updated = ndb.DateTimeProperty()
	value = ndb.FloatProperty()
	increment = ndb.FloatProperty()