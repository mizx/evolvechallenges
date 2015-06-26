import datetime
import jinja2
import os
import filters

URL_API_EVOLVE_CHALLENGE = 'http://api.4v1game.net/challenge/'
DEFAULT_CHALLENGE_KEY = 'default_challenge'
DEFAULT_CHALLENGE_DURATION = datetime.timedelta(days=3)
DEFAULT_CHALLENGE_POST_DELAY = datetime.timedelta(hours=1)
API_DATETIME_ADJUST = datetime.timedelta(hours=0)

MEMCACHE_TIME = 60*15

STRIP_TIME_BASE = '%Y-%m-%dT%H:%M:%S'
STRFTIME_JS = 'Date(%Y, %m, %d, %H, %M, %S)'
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')
    ),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENV.filters['json'] = filters.json
JINJA_ENV.filters['number'] = filters.number
JINJA_ENV.filters['percent'] = filters.percent

NUMBER_FORMAT = '{:,}'

def date_handler(obj):
	return obj.isoformat() if hasattr(obj, 'isoformat') else obj