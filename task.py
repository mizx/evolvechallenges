import datetime
import logging
import webapp2

import config
from evolve.api import EvolveApi
from models import Challenge

class ChallengeTaskHandler(webapp2.RequestHandler):

	def get(self, id=None):
		logging.info('ChallengeTaskHandler.get has been called.')
		evolve = EvolveApi()
		if id is not None:
			evolve.get_single(id)
		else:
			evolve.get_active()

class TouchTaskHandler(webapp2.RequestHandler):

	def get(self, id=None):
		logging.info('TouchTaskHandler.get has been called.')
		if id is not None:
			challenge = Challenge.query(Challenge.id == int(id)).get()
			if challenge is not None:
				challenge.put()
				logging.info('Touched challenge %s: %s' % (challenge.id, challenge.slug))
			return
		now = datetime.datetime.now()
		challenges = Challenge.query(
			Challenge.start <= now + config.DEFAULT_CHALLENGE_START_GRACE
			and Challenge.start >= now - config.DEFAULT_CHALLENGE_START_GRACE
		).fetch()
		for challenge in challenges:
			challenge.put()
			logging.info('Touched challenges %s: %s' % (challenge.id, challenge.slug))
		

app = webapp2.WSGIApplication([
    webapp2.Route(r'/task/update/<id:\d+>', ChallengeTaskHandler),
	webapp2.Route(r'/task/update/active', ChallengeTaskHandler),
	webapp2.Route(r'/task/touch/<id:\d+>', TouchTaskHandler),
	webapp2.Route(r'/task/touch', TouchTaskHandler),
], debug=config.DEV)