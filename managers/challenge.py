import config
import models
from evolve import EvolveBatch
from datetime import datetime

from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging

class ChallengeManager(object):

	def __init__(self, challenge_id=None, force_update=False):
		self.evolve = EvolveBatch(challenge_id)
		self.force_update = force_update
		self.challenges = self.evolve.fetch()
		self.__get_challenges_db()
	
	def __get_challenges_db(self):
		for challenge in self.challenges:
			challenge.db = models.challenge(challenge.id)
			if challenge.db is None:
				self.create(challenge)
			
			self.touch(challenge)
			
			if self.force_update or challenge.db.is_active:
				self.refresh_datapoints(challenge)
	
	def create(self, challenge):
		challenge.db = models.Challenge(**challenge.to_dict())
		self.send_notification(challenge.id, challenge.db.name)
	
	def touch(self, challenge):
		challenge.db.progress = challenge.progress
		challenge.db.updated = datetime.now()
		challenge.db.put()
		memcache.delete('challenge_%s' % challenge.slug)
	
	def refresh_datapoints(self, challenge):
		keys = challenge.db.get_datapoints(keys_only=True)
		ndb.delete_multi(keys)
		
		points = []
		for point in challenge.data:
			point['challenge'] = challenge.db.key
			points.append(models.ChallengeData(**point))
		
		ndb.put_multi(points)
	
	def send_notification(self, id, name):
		mail.send_mail(sender=config.MAIL_SENDER,
						to=config.MAIL_TO,
						subject='New Evolve Challenge Discovered',
						body='Challenge ID: %s Challenge Name: %s' % (id, name)
		)