import json
import webapp2
import tools

import models

class JsonBaseHandler(webapp2.RequestHandler):

	def send_json(self, data):
		self.response.headers['content-type'] = 'application/json'
		self.response.write(json.dumps(data, default=tools.json_date_handler))
	
	def raise_error(self, code):
		self.error(code)

class ChallengesHandler(JsonBaseHandler):

	def get(self, filter=None):
		challenges = [challenge.to_dict() for challenge in models.challenges(filter)]
		self.send_json(challenges)

class ChallengeHandler(JsonBaseHandler):

	def get(self, slug):
		challenge = models.challenge(slug)
		if challenge is None:
			return self.raise_error(404)
		response = challenge.to_dict()
		response['datapoints'] = [data.to_dict(exclude=['challenge']) for data in challenge.get_datapoints()]

		self.send_json(response)

app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/challenges.json', ChallengesHandler),
    webapp2.Route(r'/api/challenges/<filter>.json', ChallengesHandler),
	webapp2.Route(r'/api/challenge/<slug>.json', ChallengeHandler),
], debug=True)