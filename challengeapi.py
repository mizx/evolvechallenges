import config
import errors
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

class ChallengeApi(object):
    
    def __init__(self, id):
        self.id = id
        self.query_url = '%s%s' % (config.URL_API_EVOLVE_CHALLENGE, id)
        self._do_request()
        
    def _do_request(self):
        result = urlfetch.fetch(self.query_url)
        if result.status_code == 200:
            self._load_data(result.content)
        else:
            self.id = 0
    
    def _load_data(self, content):
        self.data = json.loads(content)
        # If you call /challenge without an id, it is in a single json list
        if type(self.data) is list and len(self.data) == 1:
            self.data = self.data[0]
        start = datetime.datetime.utcfromtimestamp(
            self.data['Configuration']['StartDateTimeEpoch']
        )
        self.data['Configuration']['StartDateTime'] = start
        end = start + config.DEFAULT_CHALLENGE_DURATION
        self.data['Configuration']['EndDateTime'] = end
        
        if self.data['Name'].contains('vs') and self.data['Configuration']['Goal'] == 50:
            self.data['Type'] = 'versus'
        else:
            self.data['Type'] = 'counter'
        
        previous_value = 0.0
        new_points = []
        for point in self.data['DataPoints']:
            time_human = point['DateTime']
            updated = datetime.datetime.strptime(time_human, config.STRIP_TIME_BASE)
            updated -= config.API_DATETIME_ADJUST
            if updated < start or updated > end + config.DEFAULT_CHALLENGE_POST_DELAY:
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
        
    
    def get_data(self):
        return self.data