import config
import models
import webapp2
import jinja2

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
