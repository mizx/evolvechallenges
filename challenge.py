import config
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import memcache

import base

class ChallengeHandler(webapp2.RequestHandler):
	def get(self, title):
		mem_key = 'challenge_%s' % title
		challenge = memcache.get(mem_key)
		if challenge is None:
			challenge = Challenge.query(Challenge.slug == title).get()
			if challenge is None:
				self.response.write('No challenge found.')
				self.error(404)
				return
			if not memcache.add(mem_key, challenge, config.MEMCACHE_TIME):
				logging.error('Memcache set failed to add key: %s' % mem_key)
		
		template = config.JINJA_ENV.get_template('challenge.html')
		self.response.write(template.render({'challenge': challenge, 'config': json.dumps(challenge.config)}))
