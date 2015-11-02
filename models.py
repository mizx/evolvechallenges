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
	type = ndb.StringProperty(choices=['counter', 'versus', 'joint', 'info'], default='counter')
	alert = ndb.StringProperty(default='')
	
	action = ndb.StringProperty(default='')
	action_stretch = ndb.StringProperty(default='')
	reward = ndb.StringProperty(default='')
	reward_stretch = ndb.StringProperty(default='')
	background = ndb.StringProperty(default='/img/bg/default.png')
	thumbnail = ndb.StringProperty(default='')
	url_news = ndb.StringProperty(default='')
	
	progress = ndb.FloatProperty(default=0.0)
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
		result['percent_time'] = self.get_time_progress()
		return result
	
	def get_datapoints(self, keys_only=False):
		return ChallengeData.query(ChallengeData.challenge==self.key).order(ChallengeData.updated).fetch(keys_only=keys_only)
	
	def is_versus(self):
		return self.type == 'versus'
	
	def is_started(self):
		return datetime.utcnow() >= self.start
	
	def is_ended(self, post_delay=True):
		if post_delay:
			return datetime.utcnow() > self.end + config.DEFAULT_CHALLENGE_POST_DELAY
		return datetime.utcnow() > self.end
	
	def is_goal_reached(self):
		return self.progress >= self.goal
	
	def is_goal_stretch_reached(self):
		return self.progress >= self.goal_stretch
	
	def get_versus_names(self):
		if not self.is_versus():
			return None
		names = self.name.split(' ')
		if len(names) >= 3 and names[1] == 'vs':
			return [names[0], names[2]]
	
	def get_time_progress(self):
		total = (self.end - self.start).total_seconds()
		remain = (self.end - self.updated).total_seconds()
		return (total - remain) / total * 100

class ChallengeData(ndb.Model):
	challenge = ndb.KeyProperty(kind=Challenge)
	updated = ndb.DateTimeProperty()
	value = ndb.FloatProperty()
	increment = ndb.FloatProperty()

def challenges(filter=None):
	query = Challenge.query()
	if type(filter) is list:
		return query.filter(Challenge.id.IN(filter)).fetch()
	if type(filter) is int:
		return query.filter(Challenge.id == filter).fetch()
	if filter == 'current':
		return query.filter(ndb.OR(Challenge.is_countdown==True, Challenge.is_active==True)).fetch()
	if filter == 'previous':
		return query.filter(Challenge.is_active != True).fetch()
	return []

def challenge(id):
	if type(id) is int:
		return Challenge.query(Challenge.id == id).get()
	if id.isdigit() or (id.startswith('-') and id[1:].isdigit()):
		return Challenge.query(Challenge.id==int(id)).get()
	return Challenge.query(Challenge.slug==id).get()