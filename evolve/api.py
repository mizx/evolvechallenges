import config
from models import Challenge, ChallengeData

from datetime import datetime
import logging
import json

from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import urlfetch

from django.template.defaultfilters import slugify

def active():
	evolve = EvolveApi()
	evolve.get_active()
	return evolve

def delete():
	options = ndb.QueryOptions(keys_only=True)
	datas = ChallengeData.query().fetch(1000, options=options)
	ndb.delete_multi(datas)

class EvolveApi(object):
	
	def __init__(self):
		self.challenges_api = []
		self.challenges_datastore = []
		self.ids = []
		self.master = {}
	
	def get_active(self):
		self.get_active_api()
		self.get_ids()
		self.get_active_datastore()
		
		self.update_challenge_datapoints()
	
	def get_active_api(self):
		self._set_url()
		return self._get_challenges()

	def get_active_datastore(self):
		for challenge in self.challenges_api:
			self.challenges_datastore.append(challenge.get_challenge_datastore())
	
	def update_challenge_datapoints(self):
		for challenge in self.challenges_api:
			challenge.put_datastore_data()
			challenge.put_datastore()
	
	def get_ids(self):
		for challenge in self.challenges_api:
			self.ids.append(challenge.get_id())
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
		self.values = []
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
		self.challenge['is_stretch'] = self.challenge.has_key('goal_stretch')
	
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
			self.values.append(datapoint['value'])
			value_previous = datapoint['value']
	
	def _process_challenge_data_calculations(self):
		self.challenge['progress'] = self._calc_max_datapoint()
		self.challenge['updated'] = datetime.now()
	
	def _calc_max_datapoint(self):
		return max(self.values) if len(values) else 0
	
	def set_key(self, key):
		self.key = key
	
	def init_challenge(self):
		self.datastore = self.to_datastore()
		self.key = self.datastore.put()
	
	def get_challenge_dict(self):
		if not len(self.challenge):
			self._process_challenge_info()
		return self.challenge
	
	def get_datapoints_dict(self):
		if not len(self.datapoints):
			self._process_challenge_data()
		return self.datapoints
	
	def get_challenge_datastore(self):
		self.datastore = Challenge.query(Challenge.id == self.id).get()
		if self.datastore is None:
			self.init_challenge()
		self.set_key(self.datastore.key)
		return self.datastore
	
	def to_datastore(self):
		return Challenge(**self.get_challenge_dict())
	
	def put_datastore(self):
		self.datastore.put()
	
	def delete_datastore_data(self):
		options = ndb.QueryOptions(keys_only=True)
		ndb.delete_multi(ChallengeData.query(ChallengeData.challenge==self.key).fetch(options=options))
	
	def put_datastore_data(self):
		self.delete_datastore_data()
		if not len(self.datapoints):
			self.get_datapoints_dict()
		ndb.put_multi(self.to_datastore_data())
	
	def to_datastore_data(self):
		datapoints = []
		for point in self.datapoints:
			point_new = ChallengeData(**point)
			point_new.challenge = self.key
			datapoints.append(point_new)
		return datapoints