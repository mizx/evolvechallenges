import admin
import api
import config
from models import Challenge
import pprint
import jinja2

import cgi
import urllib
import webapp2
import challengeapi
import challenge

from google.appengine.ext import ndb

def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.filters.update({
        # Set filters
        # ...
    })
    j.environment.globals.update({
        'uri_for': webapp2.uri_for,
    })
    return j

class BaseHandler(webapp2.RequestHandler):
    
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cashed in the app registry.
        return jinja2.get_jinja2(factory=jinja2_factory)
    
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)
    

class MainHandler(webapp2.RequestHandler):
    def get(self):
        challenge = Challenge.query().order(-Challenge.num).get()
        template_vars = {
            'challenge': challenge,
            'start': 1434855227
        }
        template = config.JINJA_ENV.get_template('countdown.html')
        self.response.write(template.render(template_vars))

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = config.JINJA_ENV.get_template('about.html')
        self.response.write(template.render({}))

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler, name='index'),
    webapp2.Route('/api/challenge_data/<id>', handler=api.ApiHandler, name="api"),
    webapp2.Route('/about', handler=AboutHandler, name='about'),
    webapp2.Route('/challenge/<title>', handler=challenge.ChallengeHandler, name='challenge'),
    #webapp2.Route('/challenges', handler=challenge.ChallengesHandler, name='challenges'),
    #webapp2.Route('/admin/update/active', handler=admin.UpdateActiveHandler, name='update.active'),
    #webapp2.Route('/admin/update/<id>', handler=admin.UpdateHandler, name='admin.update'),
    webapp2.Route('/admin/resync/<id>', handler=admin.ResyncHandler, name='admin.resync'),
    #webapp2.Route('/admin/check/new', handler=admin.CheckNewHandler, name='admin.checknew'),
], debug=True)
