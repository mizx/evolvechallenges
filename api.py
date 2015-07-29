import json
import webapp2
import tools

import models

class JsonBaseHandler(webapp2.RequestHandler):

	def send_json(self, data):
		self.response.headers['content-type'] = 'application/json'
		self.response.write(json.dumps(data, default=tools.json_date_handler))
	
	def raise_error(self):
		self.error(404)

class ChallengesHandler(JsonBaseHandler):

	def get(self):
		challenges = [challenge.to_dict() for challenge in models.challenges()]
		self.send_json(challenges)

class ChallengeHandler(JsonBaseHandler):

	def get(self, slug):
		challenge = models.challenge(slug)
		if challenge is None:
			return self.raise_error()
		self.send_json(challenge.to_dict())

app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/challenges.json', ChallengesHandler),
	webapp2.Route(r'/api/challenge/<slug>.json', ChallengeHandler),
], debug=True)