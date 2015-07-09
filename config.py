import datetime

URL_API_EVOLVE_CHALLENGE = 'http://api.4v1game.net/challenge/'
DEFAULT_CHALLENGE_DURATION = datetime.timedelta(days=3)
DEFAULT_CHALLENGE_POST_DELAY = datetime.timedelta(minutes=45)
API_DATETIME_ADJUST = datetime.timedelta(hours=0)

MEMCACHE_TIME = 60*15

NUMBER_FORMAT = '{:,}'