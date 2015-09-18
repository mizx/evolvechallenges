import models
from evolve.api import EvolveApi

from google.appengine.api import mail
import logging

class ChallengeManager(object):

	def __init__(self, challenge_id=None):
		self.evolve = EvolveApi(challenge_id)
		self.is_single = challenge_id is None
		
		self.challenges_db = []
		self.data = {}

	def run(self):
		if not self.evolve.success:
			logging.error('Evolve API Challenge call not successful. Ending challenge manager instance.')
			return
		self.get_challenges_db()
		self.touch_challenges()
		
		self.get_challenge_datapoints()
		
		
	def get_challenges_db(self):
		self.challenges_db = models.challenges(current_ids)
				
	def get_challenge_ids(self):
		ids = []
		for challenge in self.challenges_db:
			ids.append(challenge.id)
	
	def get_challenge(self, id):
		for challenge in self.challenges_db:
			if challenge.id = id:
				return challenge
		return None
	
	def touch_challenges(self):
		for id in self.evolve.get_challenge_ids():
			if id not in self.get_challenge_ids():
				self.init_challenge(id)
				continue
				
			challenge = get_challenge(id)
			if challenge is not None:
				challenge.put()
				continue
				
			logging.error('Evolve API has challenge with ID %s but was not created or found.' % id)
	
	def init_challenge(self, new_id):
		challenge = self.evolve.get_challenge(new_id)
		if challenge is None:
			logging.error('Attempted to initialize challenge with id %s, challenge from API is None' % new_id)
			continue
		
		new = models.Challenge(**challenge)
		key = new.put()
		self.challenges_db.append(new)
		
		logging.info('New challenge discovered and put in database %s.' % new_id)
		mail.send_mail(sender=config.MAIL_SENDER,
						to=config.MAIL_TO,
						subject='New Evolve Challenge Discovered',
						body='Challenge ID: %s<br>Challenge Name: %s' % (challenge.id, challenge.name)
		)
	
	def get_challenge_datapoints(self):
		for challenge in self.evolve.challenges:
			self.data[challenge.id] = {}
			self.data[challenge.id]['new'] = challenge.get_datapoints()
			self.data[challenge.id]['old'] = self.get_challenge(challenge.id).get_datapoints()
			self.data[challenge.id]['add'] = []
			self.data[challenge.id]['remove'] = []
			
		self.datapoints_add_remove()
	
	def datapoints_add_remove(self):
		for id in self.data:
			for point in self.data[id]['new']:
				if self.datapoints_find(point['updated'], self.data[id]['old'])
					self.data[id]['add'].append(point)
			
			for point in self.data[id]['old']:
				if self.datapoints_find(point['updated'], self.data[id]['new'])
					self.data[id]['remove'].append(point)
	
	def datapoints_find(self, datetime, datapoints):
		for point in datapoints:
			if datetime == point['updated']:
				return True
		return False