import config
from datetime import datetime
import re

from google.appengine.ext import ndb
from django.template.defaultfilters import slugify

class DataPoint(ndb.Model):
    #challengeId = ndb.IntegerProperty()
    updated = ndb.DateTimeProperty()
    value = ndb.FloatProperty()
    increment = ndb.FloatProperty()

class Challenge(ndb.Model):
    num = ndb.IntegerProperty(required=True)
    url = ndb.TextProperty(default="")
    name = ndb.StringProperty(required=True)
    start = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()
    slug = ndb.ComputedProperty(lambda self: slugify(self.name))
    type = ndb.StringProperty(choices=['counter', 'versus'], default='counter')
    progress = ndb.ComputedProperty(
        lambda self: (self.get_max_datapoint() / self.config['Goal']) * 100
    )
    progress_stretch = ndb.ComputedProperty(
        lambda self: (self.get_max_datapoint() / self.config['StretchGoal'] if self.has_stretch_goal() else None)
    )
    is_active = ndb.ComputedProperty(
        lambda self: (datetime.utcnow() < self.end and datetime.utcnow() > self.start)
    )
    is_achieved = ndb.ComputedProperty(
        lambda self: (self.progress >= 100 or self.type == 'versus')
    )
    config = ndb.JsonProperty()
    datapoints = ndb.StructuredProperty(DataPoint, repeated=True)
    
    def has_stretch_goal(self):
        return 'StretchGoal' in self.config
    
    def get_progress(self):
        value = int(self.progress)
        return value if value < 100 else 100
    
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
        values = []
        for point in self.datapoints:
            values.append(point.value)
        return max(self.get_datapoint_values())
    
    def get_start_seconds(self):
        return int((self.start - datetime(1970, 1, 1)).total_seconds())
    
    def get_end_seconds(self):
        return int((self.end - datetime(1970, 1, 1)).total_seconds())
    
    def get_raw_config(self):
        return self.config