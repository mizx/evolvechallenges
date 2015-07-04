import config
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2
import challengeapi

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

class ResyncHandler(webapp2.RequestHandler):
    def get(self, id):
        id = int(id)
        api = challengeapi.ChallengeApi(id)
        if api.resync():
            self.response.write('Successfully resync\'d: %s' % api)
        else:
            self.response.write('Problem occured writing: %s' % api)

class AdminHandler(webapp2.RequestHandler):
    def get(self, command=None):
        if command == 'addpreviousevents':
            insert_previous_events()

    def processData(self, results):
        return DataPoint.get_key
