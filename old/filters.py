import config
import jinja2
from json import dumps

def json(value):
    return jinja2.Markup(dumps(value))

def number(value, whole=True):
    if whole:
        return config.NUMBER_FORMAT.format(int(value))
    return config.NUMBER_FORMAT.format(value)

def percent(value):
    if value > 100:
        value = 100
    value = 100 if value > 100 else int(value)
    return '%s%%' % value