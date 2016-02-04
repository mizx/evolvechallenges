import base64
import logging
import webapp2

from google.appengine.ext import ndb

import config
from models import Challenge, ChallengeData
from datetime import datetime


class InsertDataHandler(webapp2.RequestHandler):

	def log(self, string):
		logging.info(string)
		self.response.write(string)
	
	def post(self):
		if not (self.request.remote_addr == '::1' or self.request.remote_addr == base64.b64decode(config.IP_FILTER)):
			self.abort(403)
			return
		
		now = datetime.now()
		key = self.request.POST['key']
		progress = float(self.request.POST['progress'])
		logging.info('ip address: [%s]' % self.request.remote_addr)
		
		challenge = ndb.Key(urlsafe=key).get()
		
		if now < challenge.start or now > (challenge.end + config.DEFAULT_CHALLENGE_POST_DELAY):
			self.log('Challenge is not active (now: %s, start: %s, end: %s' % (now, challenge.start, challenge.end))
			return
		
		challenge.progress = progress
		challenge.put()
		
		point = {
			'challenge': challenge.key,
			'updated': datetime.now(),
			'value': progress
		}
		data = ChallengeData(**point)
		data.put()
		self.log('updated progress')

app = webapp2.WSGIApplication([
	webapp2.Route(r'/task/script/insert/datapoint', InsertDataHandler),
], debug=config.DEV)