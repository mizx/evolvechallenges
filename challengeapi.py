import config
import errors
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from django.template.defaultfilters import slugify

class ChallengeApi(object):
    
    def __init__(self, id):
        self.id = id
        self.query_url = None
        self.url = None
        self.challenge = None
        if not self._get_datastore():
            if not self._get_http():
                self.isReady = False
                return
        self.isReady = True
        
    def _get_http(self):
        self.query_url = '%s%s' % (config.URL_API_EVOLVE_CHALLENGE, self.id)
        result = urlfetch.fetch(self.query_url)
        if result.status_code == 200:
            self._parse_data(result.content)
            return True
        else:
            self.id = 0
            return False
    
    def _get_datastore(self):
        self.challenge = Challenge.query(Challenge.num == self.id).get()
        if self.challenge is None:
            return False
        return True
    
    def resync(self):
        if self.query_url is None:
            self._get_http()
        if self.challenge is not None:
            self.delete()
        self._insert_datastore()
        return self.challenge
    
    def delete(self):
        self.url = self.challenge.url
        self.challenge.key.delete()
        
    def _insert_datastore(self):
        new_challenge = Challenge()
        new_challenge.num = self.id
        new_challenge.name = self.data['Name']
        new_challenge.type = self.data['Type']
        new_challenge.start = self.start
        new_challenge.end = self.end
        new_challenge.config = self.data['Configuration']
        for datapoint in self.data['DataPoints']:
            new_point = DataPoint()
            new_point.updated = datapoint['updated']
            new_point.value = datapoint['value']
            new_point.increment = datapoint['increment']
            new_challenge.datapoints.append(new_point)
        if self.url is not None:
            new_challenge.url = self.url
            
        new_challenge.put()
        self.challenge = new_challenge
    
    def _parse_data(self, content):
        self.data = json.loads(content)
        # If you call /challenge without an id, it is in a single json list
        if type(self.data) is list and len(self.data) == 1:
            self.data = self.data[0]
        self.start = datetime.datetime.utcfromtimestamp(
            self.data['Configuration']['StartDateTimeEpoch']
        )
        #self.data['Configuration']['StartDateTime'] = start
        self.end = self.start + config.DEFAULT_CHALLENGE_DURATION
        #self.data['Configuration']['EndDateTime'] = end
        
        if 'vs' in self.data['Name'] and self.data['Configuration']['Goal'] == 50:
            self.data['Type'] = 'versus'
        else:
            self.data['Type'] = 'counter'
        
        previous_value = 0.0
        new_points = []
        for point in self.data['DataPoints']:
            time_human = point['DateTime']
            updated = datetime.datetime.strptime(time_human, config.STRIP_TIME_BASE)
            updated -= config.API_DATETIME_ADJUST
            if updated < self.start or updated > self.end + config.DEFAULT_CHALLENGE_POST_DELAY:
                continue
                
            value = point['Value']
            new_data = {
                'value': value,
                'increment': value - previous_value,
                'updated': updated,
            }
            new_points.append(new_data)
            previous_value = value
        
        self.data['DataPoints'] = new_points
        
    def __str__(self):
        if self.data is not None:
            return 'Challenge #%s - %s' % (self.id, self.data['Name'])
        else:
            return 'Invalid Challenge'
    
    def get_data(self):
        return self.data