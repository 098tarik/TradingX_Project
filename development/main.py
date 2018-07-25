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


class CssiUser(ndb.Model):
 
  # user sign in datastore, this object stores user information
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  username = ndb.StringProperty()
  email = ndb.StringProperty()
  gender = ndb.StringProperty()
  location = ndb.StringProperty()
class Product(ndb.Model):
  #product datastore, this object stores product information
  product_name = ndb.StringProperty()
  product_description = ndb.StringProperty()
  product_picture = ndb.BlobProperty()
  trade_request = ndb.StringProperty()

#This handler allows the user to sign in at the bottom of the hompage if not logged in
class SignHandler(webapp2.RequestHandler):
 def get(self):
    	content = TEMPLATE.get_template('templates/signup.html')
        self.response.write(content.render() % (
          users.create_login_url('/')) )
          
#requests user information once that specific user is logged in the post method
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
 
#handler renders the home page html template
class HomeHandler(webapp2.RequestHandler):
    def get(self):
        content = TEMPLATE.get_template('home.html')
        self.response.write(content.render())
    
#handler allows the user to pose ONLY when they are logged in, if they are not logged in they must sign in at the bottom
#of the page
class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    content = TEMPLATE.get_template('templates/post.html')
    sign_in = TEMPLATE.get_template('templates/signin.html')
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
      self.response.write(sign_in.render())
      self.response.write('''
        Please log in to use our site! <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))
      
#requests the users product data from the post method and serves it back to the user in the post page
#class FormHandler(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    
    first_name = self.request.get('username')
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
      
    # gets and stores all user info
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
    
    #gets and stores all product info
    product_picture = self.request.get('img')
    logging.info("picture: %d" % len(product_picture))
    product_name=self.request.get('product_name')
    product_description=self.request.get('product_description')
    trade_request=self.request.get('trade_request')
    id=user.user_id()
    product = Product(product_picture=product_picture,product_name=product_name, product_description=product_description, trade_request=trade_request, id=id)
    product.put()
    #converts binary photo string to base 64 to allow it to be displayed back to the user
    s = str(product_picture).encode('base64')
    content = TEMPLATE.get_template('templates/post.html')
    self.response.write(content.render(s=s,product_name=product_name, product_description=product_description, trade_request=trade_request))
    
class ElectronicsHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().fetch()
       for post in posts:
        s = str(post.product_picture).encode('base64')
        self.response.out.write( '''
        <header>
        <br>
        <br>
    <a href="{{ signout_link_html }}" class="logout-redirect">Logout</a>
    <a href="/msg" class="message-redirect">Message</a>
    <a href="/home" class="message-redirect">Go Home</a>
    <br>
    <br>
  </header>
    <img height="100px" width="100px" src="data:image/jpg;base64,%s">
      <br>
      <br>
      <label class="product_name">Product Name: %s</label> <br>
      <label class="product_description">Product Description: %s</label> <br>
      <label class="trade_request">Willing to trade for: %s</label>
    </div>) ''' % (s,post.product_name,post.product_description,post.trade_request))
app = webapp2.WSGIApplication([
  ('/register', SignHandler),
  ('/electronics', ElectronicsHandler),
   ('/home', HomeHandler),
  ('/', MainHandler),
#  ('/new_entry', FormHandler),
  ('/U', GetUserHandler),
    ('/user', GetUserHandler),
    ('/logout', GetLogoutUrlHandler),
    ('/add', AddMessageHandler),
    ('/messages', GetMessagesHandler),
], debug=True)