import config
import errors
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

class RefreshHandler(webapp2.RequestHandler):
    def get(self, command=None):
        try:
            test = ChallengeResults()
            if command == 'all':
                
                self.response.write(test.process(True))
            else:
                self.response.write(test.process())
        except errors.CustomException as e:
            self.response.write(e.value)

    def processData(self, results):
        return DataPoint.get_key

class ChallengeResults(object):
    id = 0
    name = None
    config = None
    _raw = None
    _data = None
    _data_processed = None
    last_point = None
    current_challenge = None
    current_data = None
    current_last_point = None
    
    def getChallenge(self):
        result = urlfetch.fetch(config.URL_API_EVOLVE_CHALLENGE)
        if result.status_code == 200:
            self.init(result.content)
        if self.id == 0:
            raise errors.CustomException('No challenge id found')
    
    def init(self, results):
        self._raw = json.loads(results)
        if len(self._raw) > 0:
            self._raw = self._raw[0]
            if self._raw.has_key('Id'):
                self.id = self._raw['Id']
            if self._raw.has_key('Name'):
                self.name = self._raw['Name']
            if self._raw.has_key('Configuration'):
                self.config = self._raw['Configuration']
            if self._raw.has_key('DataPoints'):
                self._data = self._raw['DataPoints']
    
    def process(self, forceRecache=False):
        self.getChallenge()
        if forceRecache:
            return self.forceRecache()
        else:
            self.getOrCreateChallenge()
            self.getExistingDataPoints()
            self.processLastDataPoint()
    
    def forceRecache(self):
        self.forceDeleteChallenge(self.id)
        self.createChallenge()
        self.ProcessDataPoints()
        self.createAllDataPoints()
        
    def createAllDataPoints(self):
        for point in self._data_processed:
            new_point = DataPoint(
                challengeId=self.id,
                value=point['value'],
                updated=point['updated'],
                increment=point['increment']
            ).put()
    
    def forceDeleteChallenge(self, id):
        challenge = Challenge.query(Challenge.num == id).get()
        if challenge is not None:
            points = DataPoint.query(DataPoint.challengeId == id).fetch(keys_only=True)
            ndb.delete_multi(points)
            challenge.key.delete()
    
    def deleteDataPoints(self, challenge):
        points = None
        
    def getOrCreateChallenge(self):
        self.current_challenge = self.getExistingChallenge()
        if self.current_challenge is None:
            self.current_challenge = self.createChallenge()
        
    def createChallenge(self):
        new = Challenge(num = self.id, name = self.name)
        if self.config is not None:
            if self.config.has_key('Goal'):
                new.goal = self.config['Goal']
            if self.config.has_key('StartDateTimeEpoch'):
                new.start = datetime.datetime.utcfromtimestamp(
                    self.config['StartDateTimeEpoch']
                )
                new.end = new.start + config.DEFAULT_CHALLENGE_DURATION
            if self.config.has_key('YAxisLabel'):
                new.objective_name = self.config['YAxisLabel']
            if self.config.has_key('SetYMax'):
                new.objective_max = self.config['SetYMax']
            if self.config.has_key('SetYMin'):
                new.objective_min = self.config['SetYMin']
        
        new.put()
        logging.info('Created new challenge entity %s: %s' % (self.id, self.name))
        return new
    
    def getExistingChallenge(self):
        query = Challenge.query(Challenge.num == self.id)
        return query.get()
        
    def getExistingDataPoints(self):
        query = DataPoint.query(DataPoint.challengeId==self.id)
        self.current_data = query.order(-DataPoint.updated).fetch()
        if self.isCurrentDataEmpty():
            self.setLastCurrentPoint(self.current_data[0])
    
    def setLastCurrentPoint(self, value):
        self.current_last_point = value
    
    def isCurrentDataEmpty(self):
        return len(self.current_data) > 0
            
    def ProcessDataPoints(self):
        if len(self._data) > 0:
            last_value = 0
            self._data_processed = []
            for data in self._data:
                new = {}
                if data.has_key('Value') and data.has_key('DateTime'):
                    new['value'] = int(float(data['Value']))
                    new['updated'] = datetime.datetime.strptime(data['DateTime'], config.STRIP_TIME_BASE)
                    new['increment'] = new['value'] - last_value
                    self._data_processed.append(new)
                    last_value = new['value']
    
    def processLastDataPoint(self):
        if len(self._data) > 0:
            latest = self._data[-1]
            if latest.has_key('Value') and latest.has_key('DateTime'):
                value = int(float(latest['Value']))
                updated = datetime.datetime.strptime(latest['DateTime'], config.STRIP_TIME_BASE)
                if self.isNewData(updated):
                    self.createNewPoint(updated, value)
        
    def isNewData(self, latest_entry):
        if self.current_last_point is None:
            return True
        return self.current_last_point.updated < latest_entry
    
    def createNewPoint(self, updated, value):
        new_point = DataPoint(
            challengeId=self.id,
            updated=updated,
            value=value
        )
        new_point.increment = 0
        if self.current_last_point is not None:
            new_point.increment = self.current_last_point.value - value
        else:
            self.setLastCurrentPoint(new_point)
        new_point.put()
        logging.info('Successfully added new data point %s with value of %s (+%s)' % (updated, value, new_point.increment))
        
    
    
app = webapp2.WSGIApplication([
    (r'/cron/refresh/(\w+)?', RefreshHandler)
], debug=True)