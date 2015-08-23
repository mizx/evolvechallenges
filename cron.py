import config
from challengeapi import ChallengeApi
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.api import memcache

class InitHandler(webapp2.RequestHandler):
	def get(self, challenge_id):
		if challenge_id.isdigit():
			challenge_id = int(challenge_id)
		elif challenge_id.startswith('-') and challenge_id[1:].isdigit():
			challenge_id = int(challenge_id)
		else:
			self.response.write('Challenge ID is not a digit: %s' % challenge_id)
			return
		api = ChallengeApi(challenge_id)
		if api.id == 0:
			self.response.write('Invalid Challenge ID: %s' % challenge_id)
			return
		challenge = Challenge()
		challenge.num = api.id
		challenge.name = api.get_name()
		challenge.start = api.get_start_datetime()
		challenge.end = api.get_end_datetime()
		challenge.config = api.get_config()
		challenge.slug = api.get_slug()
		challenge.type = api.get_type()
		challenge.datapoints = api.get_datapoints()
		challenge.put()
		self.response.write('Successfully initialized challenge: #%s - %s' % ( challenge.num, challenge.name))
		logging.info('Successfully initialized challenge: #%s - %s' % (challenge.num, challenge.name))

class UpdateHandler(webapp2.RequestHandler):
	def get(self, challenge_id):
		if challenge_id.isdigit():
			challenge_id = int(challenge_id)
		elif challenge_id.startswith('-') and challenge_id[1:].isdigit():
			challenge_id = int(challenge_id)
		else:
			logging.error('Challenge ID is not a digit: %s' % challenge_id[1:])
			return
		challenge = Challenge.query(Challenge.num == challenge_id).get()
		if challenge is None:
			logging.error('No challenge in database with id: %s' % challenge_id)
			return
		api = ChallengeApi(challenge_id, challenge.end)
		if api.id == 0:
			logging.error('Invalid Challenge ID: %s' % challenge_id)
			return

		
		challenge.datapoints = api.get_datapoints()
		challenge.put()
		memcache.delete(challenge.memkey())
		logging.info('Successfully updated info for challenge: %s' % challenge_id)

class UpdateActiveHandler(webapp2.RequestHandler):
	def get(self):
		challenges = Challenge.query(Challenge.is_active == True).fetch()
		if not len(challenges):
			challenges = Challenge.query().filter(Challenge.end >= datetime.datetime.now()).fetch()
		
		for challenge in challenges:
			api = ChallengeApi(challenge.num)
			if api.id == 0:
				logging.error('Invalid Challenge ID: %s' % challenge.num)
				return
			challenge.datapoints = api.get_datapoints()
			challenge.put()
			memcache.delete(challenge.memkey())
			logging.info('Successfully updated info for challenge: %s' % challenge.num)


	
app = webapp2.WSGIApplication([
	webapp2.Route(r'/cron/init/<challenge_id>', handler=InitHandler, name='cron-init-challenge'),
	webapp2.Route(r'/cron/update/active', handler=UpdateActiveHandler, name='cron-update-active-challenges'),
	webapp2.Route(r'/cron/update/<challenge_id>', handler=UpdateHandler, name='cron-update-challenge'),
])