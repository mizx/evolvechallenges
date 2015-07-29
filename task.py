import webapp2

import config
from evolve.api import EvolveApi

class TaskHandler(webapp2.RequestHandler):

	def get(self, id):
		evolve = EvolveApi()
		evolve.get_single(id)

class TaskHandlerActive(webapp2.RequestHandler):

	def get(self):
		evolve = EvolveApi()
		evolve.get_active()

app = webapp2.WSGIApplication([
    webapp2.Route(r'/task/update/<id:\d+>', TaskHandler),
	webapp2.Route(r'/task/update/active', TaskHandlerActive),
], debug=config.DEV)