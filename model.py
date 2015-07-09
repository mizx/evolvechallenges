import config

from datetime import datetime
import time

from google.appengine.ext import ndb
from django.template.defaultfilters import slugify

class DataPoint(ndb.Model):
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
    img_bg = ndb.StringProperty(default="goliath_bg.jpg")
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

def AllChallenges():
    return Challenge.query()

class Guest(ndb.Model):
  first = ndb.StringProperty()
  last = ndb.StringProperty()


def AllGuests():
  return Guest.query()


def UpdateGuest(id, first, last):
  guest = Guest(id=id, first=first, last=last)
  guest.put()
  return guest


def InsertGuest(first, last):
  guest = Guest(first=first, last=last)
  guest.put()
  return guest


def DeleteGuest(id):
  key = ndb.Key(Guest, id)
  key.delete()
