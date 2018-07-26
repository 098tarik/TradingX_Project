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
class Product(ndb.Model):
  #product datastore, this object stores product information
  product_name = ndb.StringProperty()
  product_description = ndb.StringProperty()
  product_picture = ndb.BlobProperty()
  trade_request = ndb.StringProperty()
  category = ndb.StringProperty()
  
class ElectronicsHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'tech').fetch()
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
class BooksHandler(webapp2.RequestHandler):
    def get(self):
       
       posts = Product.query().filter(Product.category == 'books').fetch()
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
  <div class="row top-line animate-box">
    <img height="100px" width="100px" src="data:image/jpg;base64,%s">
      <br>
      <br>
      <label class="product_name">Product Name: %s</label> <br>
      <label class="product_description">Product Description: %s</label> <br>
      <label class="trade_request">Willing to trade for: %s</label>
    </div>) ''' % (s,post.product_name,post.product_description,post.trade_request))
class ClothesHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'clothes').fetch()
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
class GoodsHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'home_goods').fetch()
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
class ApplianceHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'appliances').fetch()
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
class MiscHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'other').fetch()
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
    