import json
import webapp2
import tools

import config
import models

from google.appengine.api import memcache

class JsonBaseHandler(webapp2.RequestHandler):

	def __init__(self, request=None, response=None):
		self.initialize(request, response)
		self.memcache_prefix = None
		self.memcache_key = None
		self.set_headers()
	
	def return_memcache(self, key, prefix=None):
		if prefix is not None:
			self.set_prefix(prefix)
		self.set_key(key)
		data_memcache = memcache.get(self.memcache_key)
		if data_memcache is not None:
			self.response.write(data_memcache)
			return True
		return False
	
	def set_headers(self):
		self.response.headers['Content-Type'] = 'application/json'
	
	def set_prefix(self, prefix):
		self.memcache_prefix = prefix
	
	def set_key(self, key):
		if self.memcache_prefix is not None:
			self.memcache_key = 'v2%s_%s' % (self.memcache_prefix, key)
		else:
			self.memcache_key = key

	def send_json(self, data):
		data_json = json.dumps(data, default=tools.json_date_handler)
		memcache.set(self.memcache_key, data_json, config.MEMCACHE_TIME)
		self.response.write(json.dumps(data, default=tools.json_date_handler))
	
	def raise_error(self, code):
		self.error(code)

class ChallengesHandler(JsonBaseHandler):

	def get(self, filter=None):
		if self.return_memcache(filter, 'filter'):
			return
		challenges = [challenge.to_dict() for challenge in models.challenges(filter)]
		self.send_json(challenges)

class ChallengeHandler(JsonBaseHandler):

	def get(self, slug):
		if self.return_memcache(slug, 'challenge'):
			return
		challenge = models.challenge(slug)
		if challenge is None:
			return self.raise_error(404)
		response = challenge.to_dict()
		response['datapoints'] = [data.to_dict(exclude=['challenge']) for data in challenge.get_datapoints()]

		self.send_json(response)

app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/challenges/<filter>.json', ChallengesHandler),
	webapp2.Route(r'/api/challenge/<slug>.json', ChallengeHandler),
], debug=True)