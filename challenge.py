import config
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import base

class ChallengeHandler(webapp2.RequestHandler):
    def get(self, title):
        challenge = Challenge.query(Challenge.slug == title).get()
        
        if challenge is None:
            self.response.write('None')
            self.error(404)
            return
        template = config.JINJA_ENV.get_template('challenge.html')
        self.response.write(template.render({'challenge': challenge, 'config': json.dumps(challenge.config)}))

class ChallengesHandler(base.BaseHandler):
    def get(self):
        challenges = Challenge.query().order(-Challenge.num).fetch(10)
        template_vars = {
            'challenges': challenges,
        }
        self.render_response('templates/challenges.html')
        return
        template = config.JINJA_ENV.get_template('challenges.html')
        self.response.write(template.render(template_vars))