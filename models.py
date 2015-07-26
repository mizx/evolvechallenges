import config

from datetime import datetime
import time

from google.appengine.ext import ndb
from django.template.defaultfilters import slugify

class DataPoint(ndb.Model):
    updated = ndb.DateTimeProperty()
    value = ndb.FloatProperty()
    increment = ndb.FloatProperty()

class News(ndb.Model):
	title = ndb.StringProperty()
	subtitle = ndb.StringProperty()
	button_text = ndb.StringProperty()
	button_link = ndb.StringProperty()

class ChallengeV2(ndb.Model):
	id = ndb.IntegerProperty(required=True)
	slug = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	
	start = ndb.DateTimeProperty(required=True)
	end = ndb.DateTimeProperty()
	type = ndb.StringProperty(choices=['counter', 'versus', 'joint'], default='counter')
	
	action = ndb.StringProperty(default='')
	reward = ndb.StringProperty(default='')
	reward_stretch = ndb.StringProperty(default='')
	background = ndb.StringProperty(default='goliath_bg.jpg')
	news_url = ndb.StringProperty(default='')
	
	progress = ndb.IntegerProperty(default=0)
	progress_stretch = ndb.IntegerProperty(default=0)
	goal = ndb.IntegerProperty(required=True)
	goal_stretch = ndb.IntegerProperty()
	is_active = ndb.ComputedProperty(
		lambda self: (datetime.utcnow() < self.end + config.DEFAULT_CHALLENGE_POST_DELAY and datetime.utcnow() > self.start)
	)
	is_achieved = ndb.ComputedProperty(lambda self: self.progress > self.goal)
	
	axis_y_min = ndb.IntegerProperty()
	axis_y_max = ndb.IntegerProperty()
	axis_y_label = ndb.StringProperty()
	
	def __str__(self):
		return self.name

class ChallengeData(ndb.Model):
	challenge = ndb.KeyProperty(kind=ChallengeV2)
	updated = ndb.DateTimeProperty()
	value = ndb.FloatProperty()
	increment = ndb.FloatProperty()

class Challenge(ndb.Model):
    num = ndb.IntegerProperty(required=True)
    url_news = ndb.TextProperty(default="")
    title = ndb.StringProperty(required=True)
    start = ndb.DateTimeProperty(required=True)
    end = ndb.DateTimeProperty()
    config = ndb.JsonProperty()
    slug = ndb.StringProperty()
    action = ndb.StringProperty(default="")
    reward = ndb.StringProperty(default="")
    background = ndb.StringProperty(default="goliath_bg.jpg")
    type = ndb.StringProperty(choices=['counter', 'versus', 'joint'], default='counter')
    progress = ndb.ComputedProperty(
        lambda self: ((self.get_max_datapoint() / self.config['Goal']) * 100)
    )
    progress_stretch = ndb.ComputedProperty(
        lambda self: ((self.get_max_datapoint() / self.config['StretchGoal']) * 100) if self.has_stretch_goal() else None
    )
    is_active = ndb.ComputedProperty(
        lambda self: (datetime.utcnow() < self.end + config.DEFAULT_CHALLENGE_POST_DELAY and datetime.utcnow() > self.start)
    )
    datapoints = ndb.StructuredProperty(DataPoint, repeated=True)
    
    def has_stretch_goal(self):
        return self.config.has_key('stretchgoal')
    
    def get_datapoint_values(self):
        values = []
        for point in self.datapoints:
            values.append(point.value)
        return values
    
    def get_datapoint_increments(self):
        inc = []
        for point in self.datapoints:
            inc.append(point.increment)
        return inc
    
    def get_avg_increment(self, hourly=True):
        increments = self.get_datapoint_increments()
        multiplier = 4 if hourly else 1
        return (sum(increments) / float(len(increments))) * 4
    
    def get_max_datapoint(self):
        values = self.get_datapoint_values()
        return max(self.get_datapoint_values()) if len(values) else 0
    
    def to_seconds(self, value):
        return int(time.mktime(value.timetuple()))
    
    def get_start_seconds(self):
        return self.to_seconds(self.start)
    
    def get_end_seconds(self):
        return self.to_seconds(self.end)

def challenges():
    return ChallengeV2.query()

def challenge(slug):
	return ChallengeV2.query(Challenge.slug == slug).get()