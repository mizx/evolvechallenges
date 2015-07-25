import config
from models import ChallengeV2, ChallengeData

from datetime import datetime
import logging
import json

from google.appengine.api import urlfetch

from django.template.defaultfilters import slugify

class EvolveApi(object):
	
	def __init__(self):
		self.test = None
		self.challenges = list()
	
	def get_active(self):
		self.url = config.URL_API_EVOLVE_CHALLENGE
		return self._get_challenges()
	
	def get_challenge(self, id):
		self.url = '%s%s' % (config.URL_API_EVOLVE_CHALLENGE, id)
		
	def _get_challenges(self):
		data = self._get_http()
		if data is None:
			return None
		self.json = json.loads(data)
		if type(self.json) is not list:
			self.json = [self.json]
		return ChallengeApi(self.json[0]).__dict__()
	
	def _get_http(self):
		result = urlfetch.fetch(self.url)
		if result.status_code != 200:
			logging.error('Unable to retrieve challenge API. Url requested: %s' % self.url)
			return None
		return result.content
	
	def get_challenges(self):
		challenges = list()
		#for challenge in self.json:

class ChallengeApi(object):
	
	def __init__(self, json):
		self.raw = json
		self.final = dict()
		self._process_data()
		
	
	def _process_data(self):
		for key in self.raw:
			if key == 'Configuration':
				for key_config in self.raw[key]:
					self.final[config.API_TO_DATASTORE[key_config]] = self.raw[key][key_config]
			elif config.API_TO_DATASTORE.has_key(key):
				self.final[config.API_TO_DATASTORE[key]] = self.raw[key]
		self._process_challenge_info()
		self._process_challenge_data()
	
	def _process_challenge_info(self):
		self.final['slug'] = slugify(self.final['name'])
		self.final['start'] = datetime.utcfromtimestamp(self.final['start'])
		self.final['end'] = self.final['start'] + config.DEFAULT_CHALLENGE_DURATION
		self.final['type'] = 'versus' if 'vs' in self.final['name'] and self.final['goal'] == 50 else 'counter'
	
	def _process_challenge_data(self):
		
	
	def __dict__(self):
		return self.final
			