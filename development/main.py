"""Simple example app to demonstrate storing info for users.
CSSI-ers!  If you want to have users log in to your site and store
info about them, here is a simple AppEngine app demonstrating
how to do that.  The typical usage is:
- First, user visits the site, and sees a message to log in.
- The user follows the link to the Google login page, and logs in.
- The user is redirected back to your app's signup page to sign
  up.
- The user then gets a page thanking them for signup.
- In the future, whenever the user is logged in, they'll see a 
  message greeting them by name.
Try logging out and logging back in with a fake email address
to create a different account (when you "log in" running your
local server, it doesn't ask for a password, and you can make
up whatever email you like).
The key piece that makes all of this work is tying the datastore
entity to the AppEngine user id, by passing the special property
id when creating the datastore entity.
cssi_user = CssiUser(..., id=user.user_id())
cssi_user.put()
and then, looking it up later by doing
cssi_user = CssiUser.get_by_id(user.user_id())
"""
import struct
import webapp2
import os
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb
import jinja2
import datetime
import json
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import logging

from google.appengine.api import memcache

TEMPLATE = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class GetLoginUrlHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {
            'url': users.create_login_url('/trade')
        }
        send_json(self, result)


def send_json(request_handler, props):
    request_handler.response.content_type = 'application/json'
    request_handler.response.out.write(json.dumps(props))



class GetLogoutUrlHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {
            'url': users.create_logout_url('/trade')
        }
        send_json(self, result)



class GetUserHandler(webapp2.RequestHandler):
    def dispatch(self):
        email = get_current_user_email()
        result = {}
        if email:
            result['user'] = email
        else:
            result['error'] = 'User is not logged in.'
        send_json(self, result)


def get_current_user_email():
    current_user = users.get_current_user()
    if current_user:
        return current_user.email()
    else:
        return None

#    ('/', GetUserHandler),
#    ('/user', GetUserHandler),


class AddMessageHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {}
        email = get_current_user_email()
        if email:
            msg_text = self.request.get('text')
            if len(msg_text) > 500:
                result['error'] = 'Message is too long.'
            elif not msg_text.strip():
                result['error'] = 'Message is empty.'
            else:
                messages = memcache.get('messages')
                if not messages:
                    messages = []
                msg = Message(email, msg_text)
                messages.append(msg)
                memcache.set('messages', messages)
                result['OK'] = True
        else:
            result['error'] = 'User is not logged in.'
        send_json(self, result)



class GetMessagesHandler(webapp2.RequestHandler):
    def dispatch(self):
        result = {}
        email = get_current_user_email()
        if email:
            result['messages'] = []
            messages = memcache.get('messages')
            if messages:
                for message in messages:
                    result['messages'].append(message.to_dict())
        else:
            result['error'] = 'User is not logged in.'
        send_json(self, result)
# add this mapping to your app
#     ('/messages', GetMessagesHandler),


class Message(object):
    def __init__(self, email, text):
        self.email = email
        self.text = text
        self.timestamp = datetime.datetime.now()
    def to_dict(self):
        result = {
            'email': self.email,
            'text': self.text,
            #'time': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            'time': self.timestamp.strftime('%I:%M:%S')
        }
        return result
class UserPhoto(ndb.Model):
    user = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()

class CssiUser(ndb.Model):
  """CssiUser stores information about a logged-in user.
  The AppEngine users api stores just a couple of pieces of
  info about logged-in users: a unique id and their email address.
  If you want to store more info (e.g. their real name, high score,
  preferences, etc, you need to create a Datastore model like this
  example).  
  """
  
  # user sign in datastore
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  username = ndb.StringProperty()
  email = ndb.StringProperty()
  gender = ndb.StringProperty()
  location = ndb.StringProperty()
class Product(ndb.Model):
  #product post datastore
  product_name = ndb.StringProperty()
  product_description = ndb.StringProperty()
  product_picture = ndb.BlobProperty()
  trade_request = ndb.StringProperty()

class SignHandler(webapp2.RequestHandler):
 def get(self):
    	content = TEMPLATE.get_template('templates/signup.html')
        self.response.write(content.render() % (
          users.create_login_url('/')) )
        
 def post(self):
    user = users.get_current_user()
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
    cssi_user= CssiUser(
        first_name=self.request.get('firstname'),
        last_name=self.request.get('lastname'),
        username=self.request.get('Username'),
        gender=self.request.get('gender'),
        email=self.request.get('Email'),
        id=user.user_id())
    cssi_user.put()
    self.redirect('/')
 
class HomeHandler(webapp2.RequestHandler):
    def get(self):
        content = TEMPLATE.get_template('home.html')
        self.response.write(content.render())
    
class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    content = TEMPLATE.get_template('templates/post.html')
    # If the user is logged in...
    if user:
    
      email_address = user.nickname()
      cssi_user = CssiUser.get_by_id(user.user_id())
      upload_url = blobstore.create_upload_url('/upload_photo')
      signout_link_html =  users.create_logout_url('/')
      # If the user has previously been to our site, we greet them!
      if cssi_user:
        self.response.write(content.render(signout_link_html=signout_link_html))
      # If the user hasn't been to our site, we ask them to sign up
      elif cssi_user == None:
        self.redirect('/register')
    # Otherwise, the user isn't logged in!
    else:
      self.response.write('''
        Please log in to use our site! <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))

#class FormHandler(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    
    first_name = self.request.get('username')
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
    first_name=self.request.get('firstname')
    last_name=self.request.get('lastname')
    username=self.request.get('Username')
    gender=self.request.get('gender')
    email=self.request.get('Email')
    cssi_user= CssiUser(first_name=first_name,
    last_name=last_name,
    username=username,
    gender=gender,
    email=email)
    product_picture = self.request.get('img')
    logging.info("picture: %d" % len(product_picture))
    product_name=self.request.get('product_name')
    product_description=self.request.get('product_description')
    trade_request=self.request.get('trade_request')
    id=user.user_id()
    product = Product(product_picture=product_picture,product_name=product_name, product_description=product_description, trade_request=trade_request, id=id)
    product.put()
    s = str(product_picture).encode('base64')
    content = TEMPLATE.get_template('templates/post.html')
    self.response.write(content.render(s=s,product_name=product_name, product_description=product_description, trade_request=trade_request))
    
#class Image(webapp2.RequestHandler):
#    def get(self):
#        greeting_key = ndb.Key(urlsafe=self.request.get('img'))
#        greeting = greeting_key.get()
#        if greeting.avatar:
#            self.response.headers['Content-Type'] = 'image/png'
#            self.response.out.write(greeting.avatar)
#        else:
#            self.response.out.write('No image')
app = webapp2.WSGIApplication([
  ('/register', SignHandler),
   ('/home', HomeHandler),
  ('/', MainHandler),
#  ('/new_entry', FormHandler),
  ('/U', GetUserHandler),
    ('/user', GetUserHandler),
    ('/logout', GetLogoutUrlHandler),
    ('/add', AddMessageHandler),
    ('/messages', GetMessagesHandler),
], debug=True)