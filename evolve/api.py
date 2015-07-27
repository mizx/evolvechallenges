import config
from models import ChallengeV2, ChallengeData

from datetime import datetime
import logging
import json

from google.appengine.api import mail
from google.appengine.api import urlfetch

from django.template.defaultfilters import slugify

def active():
	evolve = EvolveApi()
	for challenge in evolve.get_active():
		print challenge.to_datastore()
	return evolve

class EvolveApi(object):
	
	def __init__(self):
		self.challenges_api = []
		self.challenges_datastore = []
		self.ids = []
	
	def get_active(self):
		self.get_active_api()
		self.get_active_datastore()
		self.get_ids()
		if len(self.challenges_api) != self.challenges_datastore:
			
	
	def get_active_api(self):
		self._set_url()
		return self._get_challenges()
	
	def get_active_datastore(self):
		self.challenges_datastore = ChallengeV2.query(ChallengeV2.id.IN([self.ids])).fetch()
	
	def get_ids(self):
		for challenge in self.challenges_api:
			self.ids.append(challenge.id)
		return self.ids
	
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
		self.challenges_api = []
		if type(self.json) is not list:
			self.json = [self.json]
		for challenge in self.json:
			self.challenges_api.append(ChallengeApi(challenge))
			
		return self.challenges_api
	
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
		self.json = json
		self.challenge = {}
		self.datastore = None
		self.datapoints = []
		self.id = None
		self.key = None
	
	def get_id(self):
		if not len(self.challenge):
			self._process_challenge_info()
		return self.id
	
	def _process_challenge_info(self):
		for key in self.json:
			if key == 'Configuration':
				for key_config in self.json[key]:
					self.challenge[config.API_TO_DATASTORE[key_config]] = self.json[key][key_config]
			elif config.API_TO_DATASTORE.has_key(key):
				self.challenge[config.API_TO_DATASTORE[key]] = self.json[key]
		
		self.id = self.challenge['id']
		self._process_challenge_extras()
	
	def _process_challenge_extras(self):
		self.challenge['slug'] = slugify(self.challenge['name'])
		self.challenge['start'] = datetime.utcfromtimestamp(self.challenge['start'])
		self.challenge['end'] = self.challenge['start'] + config.DEFAULT_CHALLENGE_DURATION
		self.challenge['type'] = 'versus' if 'vs' in self.challenge['name'] and self.challenge['goal'] == 50 else 'counter'
	
	def _process_challenge_data(self):
		value_previous = 0.0
		
		start = self.challenge['start']
		end = self.challenge['end'] + config.DEFAULT_CHALLENGE_POST_DELAY
		
		for point in self.json['DataPoints']:
			datapoint = {}
			datapoint['updated'] = datetime.strptime(point['DateTime'], config.STRIP_TIME_BASE)
			
			if datapoint['updated'] < start or datapoint['updated'] > end:
				continue
			
			datapoint['value'] = point['Value']
			datapoint['increment'] = datapoint['value'] - value_previous
			
			self.datapoints.append(datapoint)
			value_previous = datapoint['value']
	
	def init_challenge(self):
		self.key = self.to_datastore.put()
	
	def get_challenge_dict(self):
		if not len(self.challenge):
			self._process_challenge_info()
		return self.challenge
	
	def get_datapoints_dict(self):
		if not len(self.datapoints):
			self._process_challenge_data()
		return self.datapoints
	
	def get_challenge_datastore(self):
		self.datastore = ChallengeV2.query(ChallengeV2.id == self.id).get()
		if self.datastore is None:
			self.init_challenge()
		return self.datastore
	
	def to_datastore(self):
		return ChallengeV2(**self.get_challenge_dict())
	
	def to_datastore_data(self, challenge_key):
		datapoints = []
		for point in self.datapoints:
			point_new = ChallengeData(**self.datapoints)
			point_new.challenge = challenge_key
			datapoints.append(point_new)
		return datapoints