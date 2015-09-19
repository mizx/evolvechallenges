import datetime
import os
import base64

#DEV = os.environ['SERVER_SOFTWARE'].startswith('Dev')
DEV = False

URL_API_EVOLVE_CHALLENGE = 'http://challenge.4v1game.net/challenge/'

if DEV:
	URL_API_EVOLVE_CHALLENGE = 'http://mizx.me/evolve/challenge/'
	

DEFAULT_CHALLENGE_DURATION = datetime.timedelta(days=3)
DEFAULT_CHALLENGE_POST_DELAY = datetime.timedelta(minutes=30)
DEFAULT_CHALLENGE_START_GRACE = datetime.timedelta(minutes=5)
API_DATETIME_ADJUST = datetime.timedelta(hours=0)

MEMCACHE_TIME = 60*15

STRIP_TIME_BASE = '%Y-%m-%dT%H:%M:%S'

MAIL_SENDER = 'EvolveChallenges.com Automation <noreply@evolvechallenges.com>'
MAIL_TO = base64.b64decode('Q29keSBNYXRoaXNlbiA8Y29keWxtYXRoaXNlbkBnbWFpbC5jb20+') # only smart bots can have my email...

NUMBER_FORMAT = '{:,}'

API_TO_DATASTORE = {
	'Id': 'id',
	'Name': 'name',
	'Goal': 'goal',
	'Type': 'type',
	'Action': 'action',
	'Background': 'background',
	'Thumbnail': 'thumbnail',
	'Reward': 'reward',
	'NewsUrl': 'url_news',
	'StretchGoal': 'goal_stretch',
	'StartDateTimeEpoch': 'start',
	'EndDateTimeEpoch': 'end',
	'YAxisLabel': 'axis_y_label',
	'SetYMin': 'axis_y_min',
	'SetYMax': 'axis_y_max',
}