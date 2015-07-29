import datetime

DEV = True

if DEV:
	URL_API_EVOLVE_CHALLENGE = 'http://mizx.me/evolve/challenge/'
else:
	URL_API_EVOLVE_CHALLENGE = 'http://challenge.4v1game.net/challenge/'

DEFAULT_CHALLENGE_DURATION = datetime.timedelta(days=3)
DEFAULT_CHALLENGE_POST_DELAY = datetime.timedelta(minutes=30)
API_DATETIME_ADJUST = datetime.timedelta(hours=0)

MEMCACHE_TIME = 60*15

STRIP_TIME_BASE = '%Y-%m-%dT%H:%M:%S'

NUMBER_FORMAT = '{:,}'

API_TO_DATASTORE = {
	'Id': 'id',
	'Name': 'name',
	'Goal': 'goal',
	'StretchGoal': 'goal_stretch',
	'StartDateTimeEpoch': 'start',
	'YAxisLabel': 'axis_y_label',
	'SetYMin': 'axis_y_min',
	'SetYMax': 'axis_y_max'
}