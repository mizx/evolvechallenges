import config
from models import ChallengeV2, ChallengeData

from datetime import datetime
import logging
import json

from google.appengine.api import mail
from google.appengine.api import urlfetch

from django.template.defaultfilters import slugify

class EvolveApi(object):
	
	def __init__(self):
		self.test = None
		self.challenges = list()
	
	def get_active(self):
		self._set_url()
		return self._get_challenges()
	
	def active_check(self):
		self._set_url()
	
	def get_challenge(self, id):
		self._set_url(id)
	
	def _set_url(self, id=None):
		if id is not None:
			self.url = '%s%s' % (config.URL_API_EVOLVE_CHALLENGE, id)
			return
		self.url = config.URL_API_EVOLVE_CHALLENGE
		
	def _get_challenges(self):
		data = self._get_http()
		if data is None:
			return None
		self.json = json.loads(data)
		self.challenges = []
		if type(self.json) is not list:
			self.json = [self.json]
		for challenge in self.json:
			self.challenges.append(ChallengeApi(challenge))
			
		return self.challenges
	
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
		self.challenge = {}
		self.datapoints = []
		self._process_data()
		
	
	def _process_data(self):
		for key in self.raw:
			if key == 'Configuration':
				for key_config in self.raw[key]:
					self.challenge[config.API_TO_DATASTORE[key_config]] = self.raw[key][key_config]
			elif config.API_TO_DATASTORE.has_key(key):
				self.challenge[config.API_TO_DATASTORE[key]] = self.raw[key]
		self._process_challenge_info()
		self._process_challenge_data()
	
	def _process_challenge_info(self):
		self.challenge['slug'] = slugify(self.challenge['name'])
		self.challenge['start'] = datetime.utcfromtimestamp(self.challenge['start'])
		self.challenge['end'] = self.challenge['start'] + config.DEFAULT_CHALLENGE_DURATION
		self.challenge['type'] = 'versus' if 'vs' in self.challenge['name'] and self.challenge['goal'] == 50 else 'counter'
	
	def _process_challenge_data(self):
		value_previous = 0.0
		
		start = self.challenge['start']
		end = self.challenge['end'] + config.DEFAULT_CHALLENGE_POST_DELAY
		
		for point in self.raw['DataPoints']:
			datapoint = {}
			datetime_human = ['DateTime']
			datapoint['updated'] = datetime.strptime(datetime_human, config.STRIP_TIME_BASE)
			
			if datapoint['updated'] < start or datapoint['updated'] > end:
				continue
			
			datapoint['value'] = point['Value']
			datapoint['increment'] = datapoint['value'] - value_previous
			
			self.datapoints.append(datapoint)
			value_previous = datapoint['value']
		
	
	def to_dict(self):
		return self.challenge
	
	def to_datastore(self):
		return ChallengeV2(**self.to_dict())
	
	def to_datastore_data(self):
		return [