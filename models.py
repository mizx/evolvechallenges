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

class ClassType(ndb.Model):
	name = ndb.StringProperty()
	is_hunter = ndb.BooleanProperty()

class Character(ndb.Model):
	name = ndb.StringProperty()
	class_type = ndb.KeyProperty(kind=ClassType)

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
	action_stretch = ndb.StringProperty(default='')
	reward = ndb.StringProperty(default='')
	reward_stretch = ndb.StringProperty(default='')
	background = ndb.StringProperty(default='/img/bg/default.png')
	thumbnail = ndb.StringProperty(default='')
	url_news = ndb.StringProperty(default='')
	
	progress = ndb.FloatProperty(default=0)
	goal = ndb.IntegerProperty(required=True)
	goal_stretch = ndb.IntegerProperty()
	is_stretch = ndb.ComputedProperty(
		lambda self: self.goal_stretch is not None and self.goal_stretch > 0
	)
	is_countdown = ndb.ComputedProperty(lambda self: not self.is_started())
	is_active = ndb.ComputedProperty(
		lambda self: (not self.is_ended() and self.is_started())
	)
	is_achieved = ndb.ComputedProperty(
		lambda self: self.is_ended() if self.is_versus() else self.is_goal_reached()
	)
	is_achieved_stretch = ndb.ComputedProperty(
		lambda self: self.is_goal_stretch_reached() if self.is_stretch else False
	)
	
	axis_y_min = ndb.IntegerProperty()
	axis_y_max = ndb.IntegerProperty()
	axis_y_label = ndb.StringProperty()
	
	@classmethod
	def _get_kind(cls):
		return 'Challenge2'
	
	def to_dict(self):
		result = super(Challenge, self).to_dict()
		if self.is_versus():
			result['versus_names'] = self.get_versus_names()
		return result
	
	def get_datapoints(self):
		return ChallengeData.query(ChallengeData.challenge==self.key).order(ChallengeData.updated).fetch()
	
	def is_versus(self):
		return self.type == 'versus'
	
	def is_started(self):
		return datetime.utcnow() >= self.start
	
	def is_ended(self, post_delay=True):
		if post_delay:
			return datetime.utcnow() > self.end + config.DEFAULT_CHALLENGE_POST_DELAY
		return datetime.utcnow() > self.end
	
	def is_goal_reached(self):
		return self.progress > self.goal
	
	def is_goal_stretch_reached(self):
		return self.progress > self.goal_stretch
	
	def get_versus_names(self):
		if not self.is_versus():
			return None
		names = self.name.split(' ')
		if len(names) >= 3 and names[1] == 'vs':
			return [names[0], names[2]]

class ChallengeData(ndb.Model):
	challenge = ndb.KeyProperty(kind=Challenge)
	updated = ndb.DateTimeProperty()
	value = ndb.FloatProperty()
	increment = ndb.FloatProperty()

def challenges(filter=None):
	if filter == 'countdown':
		return Challenge.query(Challenge.is_countdown==True).fetch()
	return Challenge.query().fetch()

def challenge(slug):
	return Challenge.query(Challenge.slug==slug).get()