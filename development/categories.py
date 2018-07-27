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
       if posts:
	       for post in posts:
	        s = str(post.product_picture).encode('base64')
	        self.response.out.write( '''
	        <!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	          <br>
	        <br>
	    <br>
	    <br>
	  </header>
	  <style> body {

background-image: url("https://raw.githubusercontent.com/noyoshi/wallpapers/master/kzg_space.jpg");

} </style>
	  <body>
	   <div align="center">
	    <img height="300px" width="300px" src="data:image/jpg;base64,%s">
	      <br>
	      <br>
	      <label class="product_name">Product Name: %s</label> <br>
	      <label class="product_description">Product Description: %s</label> <br>
	      <label class="trade_request">Willing to trade for: %s</label> <br>
	    <a href="/msg" class="message-redirect">
	    <button>Message</button></a>
	    <a href="/home" class="message-redirect">
	    <button>Go Home</button></a>
	      </div>
	    </div>
	''' % (s,post.product_name,post.product_description,post.trade_request))
       else:
    		self.response.write('''<!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <a href="{{ signout_link_html }}" class="logout-redirect">Post</a>
	    <a href="/msg" class="message-redirect">Message</a>
	    <a href="/home" class="message-redirect">Go Home</a>
	    <br>
	    <br>
	  </header> <body> <p class="no_post_page"> MAKE A POST!</P> </body>
	  <footer id="fh5co-footer" role="contentinfo">
		<div class="container">
			<div class="row copyright">
				<div class="col-md-12 text-center">
					<p>
						<small class="block">&copy; 2018 TradingX. All Rights Reserved.</small>
					</p>
					<ul class="fh5co-social-icons">
						<li><a href="#"><i class="icon-twitter"></i></a></li>
						<li><a href="#"><i class="icon-facebook"></i></a></li>
						<li><a href="#"><i class="icon-instagram"></i></a></li>
					</ul>
				</div>
			</div>
		</div>
	</footer>''')
    
    
    
    
    
    
class BooksHandler(webapp2.RequestHandler):
    def get(self): 
       posts = Product.query().filter(Product.category == 'books').fetch()
       if posts:
	       for post in posts:
	        s = str(post.product_picture).encode('base64')
	        self.response.out.write( '''
	        <!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <br>
	    <br>
	  </header>
	  <style> body {

background-image: url("https://raw.githubusercontent.com/noyoshi/wallpapers/master/kzg_space.jpg");

} </style>
	  <body>
	   <div align="center">
	    <img height="300px" width="300px" src="data:image/jpg;base64,%s">
	      <br>
	      <br>
	      <label class="product_name">Product Name: %s</label> <br>
	      <label class="product_description">Product Description: %s</label> <br>
	      <label class="trade_request">Willing to trade for: %s</label> <br>
	    <a href="/msg" class="message-redirect">
	    <button>Message</button></a>
	    <a href="/home" class="message-redirect">
	    <button>Go Home</button></a>
	      </div>
	      
	    </div></body> ''' % (s,post.product_name,post.product_description,post.trade_request))
       else:
    		self.response.write('''<!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <a href="{{ signout_link_html }}" class="logout-redirect">Logout</a>
	    <a href="/msg" class="message-redirect">Message</a>
	    <a href="/home" class="message-redirect">Go Home</a>
	    <br>
	    <br>
	  </header> <body> <p class="no_post_page"> MAKE A POST!</P> </body>
	  <footer id="fh5co-footer" role="contentinfo">
		<div class="container">
			<div class="row copyright">
				<div class="col-md-12 text-center">
					<p>
						<small class="block">&copy; 2018 TradingX. All Rights Reserved.</small>
					</p>
					<ul class="fh5co-social-icons">
						<li><a href="#"><i class="icon-twitter"></i></a></li>
						<li><a href="#"><i class="icon-facebook"></i></a></li>
						<li><a href="#"><i class="icon-instagram"></i></a></li>
					</ul>
				</div>
			</div>
		</div>
	</footer>''')
    
    
    
    
    
class ClothesHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'clothes').fetch()
       if posts:
	       for post in posts:
	        s = str(post.product_picture).encode('base64')
	        self.response.out.write( '''
	        <!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	       <br>
	        <br>
	    <br>
	    <br>
	  </header>
	  <style> body {

background-image: url("https://raw.githubusercontent.com/noyoshi/wallpapers/master/kzg_space.jpg");

} </style>
	  <body>
	   <div align="center">
	    <img height="300px" width="300px" src="data:image/jpg;base64,%s">
	      <br>
	      <br>
	      <label class="product_name">Product Name: %s</label> <br>
	      <label class="product_description">Product Description: %s</label> <br>
	      <label class="trade_request">Willing to trade for: %s</label> <br>
	    <a href="/msg" class="message-redirect">
	    <button>Message</button></a>
	    <a href="/home" class="message-redirect">
	    <button>Go Home</button></a>
	      </div>
	    </div>''' % (s,post.product_name,post.product_description,post.trade_request))
       else:
    		self.response.write('''<!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <a href="/msg" class="message-redirect">Message</a>
	    <a href="/home" class="message-redirect">Go Home</a>
	    <br>
	    <br>
	  </header> <body> <p class="no_post_page"> MAKE A POST!</P> </body>
	  <footer id="fh5co-footer" role="contentinfo">
		<div class="container">
			<div class="row copyright">
				<div class="col-md-12 text-center">
					<p>
						<small class="block">&copy; 2018 TradingX. All Rights Reserved.</small>
					</p>
					<ul class="fh5co-social-icons">
						<li><a href="#"><i class="icon-twitter"></i></a></li>
						<li><a href="#"><i class="icon-facebook"></i></a></li>
						<li><a href="#"><i class="icon-instagram"></i></a></li>
					</ul>
				</div>
			</div>
		</div>
	</footer>''')
    
    
    
    
    
    
    
class GoodsHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'home_goods').fetch()
       if posts:
	       for post in posts:
	        s = str(post.product_picture).encode('base64')
	        self.response.out.write( '''
	        <!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <br>
	    <br>
	    <style> body {

background-image: url("https://raw.githubusercontent.com/noyoshi/wallpapers/master/kzg_space.jpg");

} </style>
	    <body>
	  </header>
	 <div align="center">
	    <img height="300px" width="300px" src="data:image/jpg;base64,%s">
	      <br>
	      <br>
	      <label class="product_name">Product Name: %s</label> <br>
	      <label class="product_description">Product Description: %s</label> <br>
	      <label class="trade_request">Willing to trade for: %s</label> <br>
	    <a href="/msg" class="message-redirect">
	    <button>Message</button></a>
	    <a href="/home" class="message-redirect">
	    <button>Go Home</button></a>
	      </div>
	      
	    </div> </body>''' % (s,post.product_name,post.product_description,post.trade_request))
       else:
    		self.response.write('''<!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <a href="{{ signout_link_html }}" class="logout-redirect">Post</a>
	    <a href="/msg" class="message-redirect">Message</a>
	    <a href="/home" class="message-redirect">Go Home</a>
	    <br>
	    <br>
	  </header> <body> <p class="no_post_page"> MAKE A POST!</P> </body>
	  <footer id="fh5co-footer" role="contentinfo">
		<div class="container">
			<div class="row copyright">
				<div class="col-md-12 text-center">
					<p>
						<small class="block">&copy; 2018 TradingX. All Rights Reserved.</small>
					</p>
					<ul class="fh5co-social-icons">
						<li><a href="#"><i class="icon-twitter"></i></a></li>
						<li><a href="#"><i class="icon-facebook"></i></a></li>
						<li><a href="#"><i class="icon-instagram"></i></a></li>
					</ul>
				</div>
			</div>
		</div>
	</footer>''')
    
    
    
    
    
    
    
    
class ApplianceHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'appliances').fetch()
       if posts:
	       for post in posts:
	        s = str(post.product_picture).encode('base64')
	        self.response.out.write( '''
	        <!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	   
	    <br>
	    <br>
	  </header>
	  <style> body {

background-image: url("https://raw.githubusercontent.com/noyoshi/wallpapers/master/kzg_space.jpg");

} </style>
	  <body>
	   <div align="center">
	    <img height="300px" width="300px" src="data:image/jpg;base64,%s">
	      <br>
	      <br>
	      <label class="product_name">Product Name: %s</label> <br>
	      <label class="product_description">Product Description: %s</label> <br>
	      <label class="trade_request">Willing to trade for: %s</label> <br>
	    <a href="/msg" class="message-redirect">
	    <button>Message</button></a>
	    <a href="/home" class="message-redirect">
	    <button>Go Home</button></a>
	      </div>
	      
	    </div></body> ''' % (s,post.product_name,post.product_description,post.trade_request))
       else:
    		self.response.write('''<!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <a href="/msg" class="message-redirect">Message</a>
	    <a href="/home" class="message-redirect">Go Home</a>
	    <br>
	    <br>
	  </header> <body> <p class="no_post_page"> MAKE A POST!</P> </body>
	  <footer id="fh5co-footer" role="contentinfo">
		<div class="container">
			<div class="row copyright">
				<div class="col-md-12 text-center">
					<p>
						<small class="block">&copy; 2018 TradingX. All Rights Reserved.</small>
					</p>
					<ul class="fh5co-social-icons">
						<li><a href="#"><i class="icon-twitter"></i></a></li>
						<li><a href="#"><i class="icon-facebook"></i></a></li>
						<li><a href="#"><i class="icon-instagram"></i></a></li>
					</ul>
				</div>
			</div>
		</div>
	</footer>''')
    
    
    
    
    
    
    
class MiscHandler(webapp2.RequestHandler):
    def get(self):
       posts = Product.query().filter(Product.category == 'other').fetch()
       if posts:
	       for post in posts:
	        s = str(post.product_picture).encode('base64')
	        self.response.out.write( '''
	        <!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <br>
	    <br>
	  </header>
	   <style> body {

background-image: url("https://raw.githubusercontent.com/noyoshi/wallpapers/master/kzg_space.jpg");

} </style>
	  <body>
	  
	  <div align="center">
	    <img height="300px" width="300px" src="data:image/jpg;base64,%s">
	      <br>
	      <br>
	      <label class="product_name">Product Name: %s</label> <br>
	      <label class="product_description">Product Description: %s</label> <br>
	      <label class="trade_request">Willing to trade for: %s</label> <br>
	    <a href="/msg" class="message-redirect">
	    <button>Message</button></a>
	    <a href="/home" class="message-redirect">
	    <button>Go Home</button></a>
	      </div>
	      
	    </div> </body> ''' % (s,post.product_name,post.product_description,post.trade_request))
       else:
    		self.response.write('''<!-- Animate.css -->
			<link rel="stylesheet" href="css/animate.css">
			<!-- Icomoon Icon Fonts-->
			<link rel="stylesheet" href="css/icomoon.css">
			<!-- Bootstrap  -->
			<link rel="stylesheet" href="css/bootstrap.css">
			<!-- Theme style  -->
			<link rel="stylesheet" href="css/style.css">
			<nav class="fh5co-nav" role="navigation">
				<div class="container">
					<div class="fh5co-top-logo">
						<div id="fh5co-logo"><a href="/home">TradingX</a></div>
					</div>
				<div class="fh5co-top-menu menu-1 text-center">
				</div>
				<div class="fh5co-top-social menu-1 text-right">
					<p><a href="/" class="btn btn-primary" id="login_button">Post</a></p>
				</div>
				</div>
			</nav>
	        <header>
	        <br>
	        <br>
	    <a href="/msg" class="message-redirect">Message</a>
	    <a href="/home" class="message-redirect">Go Home</a>
	    <br>
	    <br>
	  </header> <body> <p class="no_post_page"> MAKE A POST!</P> </body>
	  <footer id="fh5co-footer" role="contentinfo">
		<div class="container">
			<div class="row copyright">
				<div class="col-md-12 text-center">
					<p>
						<small class="block">&copy; 2018 TradingX. All Rights Reserved.</small>
					</p>
					<ul class="fh5co-social-icons">
						<li><a href="#"><i class="icon-twitter"></i></a></li>
						<li><a href="#"><i class="icon-facebook"></i></a></li>
						<li><a href="#"><i class="icon-instagram"></i></a></li>
					</ul>
				</div>
			</div>
		</div>
	</footer>''')