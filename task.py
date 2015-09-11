import datetime
import logging
import webapp2

from google.appengine.ext import ndb

import config
from evolve.api import EvolveApi
from models import Challenge
import models

class TaskHandler(webapp2.RequestHandler):
	
	def log(self, string):
		logging.info(string)
		self.response.write(string)

class ChallengeTaskHandler(TaskHandler):

	def get(self, id=None):
		self.log('ChallengeTaskHandler.get has been called with id=%s' % id)
		evolve = EvolveApi()
		if id is not None:
			evolve.get_single(id)
		else:
			evolve.get_active()

class TouchTaskHandler(TaskHandler):

	def get(self, id=None):
		self.log('TouchTaskHandler.get has been called.')
		if id is not None:
			challenge = Challenge.query(Challenge.id == int(id)).get()
			if challenge is not None:
				challenge.put()
				self.log('Touched challenge %s: %s' % (challenge.id, challenge.slug))
			return
		now = datetime.datetime.now()
		challenges = Challenge.query(
			Challenge.start <= now + config.DEFAULT_CHALLENGE_START_GRACE
			and Challenge.start >= now - config.DEFAULT_CHALLENGE_START_GRACE
		).fetch()
		for challenge in challenges:
			challenge.put()
			self.log('Touched challenges %s: %s' % (challenge.id, challenge.slug))

class DeleteTaskHandler(TaskHandler):

	def get(self, id):
		self.log('DeleteTaskHandler.get has been called.')
		challenge = models.challenge(id)
		if challenge is not None:
			self.log('Deleting challenge %s' % challenge.slug)
			datapoints = challenge.get_datapoints(keys_only=True)
			ndb.delete_multi(datapoints)
			challenge.key.delete()
			

app = webapp2.WSGIApplication([
    webapp2.Route(r'/task/update/active', ChallengeTaskHandler),
	webapp2.Route(r'/task/update/<id>', ChallengeTaskHandler),
	webapp2.Route(r'/task/touch/<id>', TouchTaskHandler),
	webapp2.Route(r'/task/touch', TouchTaskHandler),
	webapp2.Route(r'/task/delete/<id>', DeleteTaskHandler),
], debug=config.DEV)