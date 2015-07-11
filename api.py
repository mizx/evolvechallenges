import json
import webapp2
import tools

import model

class JsonBaseHandler(webapp2.RequestHandler):

	def send_json(self, data):
		self.response.headers['content-type'] = 'application/json'
		self.response.write(json.dumps(data, default=tools.json_date_handler))
	
	def raise_error(self):
		self.error(404)

class ChallengesHandler(JsonBaseHandler):

	def get(self):
		# TODO: Memcache
		data = []
		for challenge in model.challenges():
			data_max = challenge.get_max_datapoint()
			challenge = challenge.to_dict()
			challenge['progress_raw'] = data_max
			del challenge['datapoints']
			data.append(challenge)
		
		self.send_json(data)

class ChallengeHandler(JsonBaseHandler):

	def get(self, slug):
		challenge = model.challenge(slug)
		if challenge is None:
			return self.raise_error()
		self.send_json(challenge.to_dict())

app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/challenges.json', ChallengesHandler),
	webapp2.Route(r'/api/challenge/<slug>.json', ChallengeHandler),
], debug=True)