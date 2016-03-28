#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import logging
import jinja2

# Lets set it up so we know where we stored the template files
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
		current_page = self.request.path
		logging.info("Current path: " + current_page)
		title = ""
		index_large = False
		food_large = False
		family_large = False
		if "index" in current_page:
			title = "Home"
			index_large = True
		elif "food" in current_page:
			title = "Food"
			food_large = True
		elif "family" in current_page:	# current_page == "/family.html"
			title = "Family"
			family_large = True
		else:
			current_page += "index.html"
			title = "Home"
			index_large = True
		template_values = {
			"title": title,
			"index_large": index_large,
			"food_large": food_large,
			"family_large": family_large,
			"login_large": False
		}
		template = JINJA_ENVIRONMENT.get_template('templates' + current_page)
		self.response.write(template.render(template_values))

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		logging.info("Current path: " + self.request.path)
		template_values = {
			"title": "Login",
			"index_large": False,
			"food_large": False,
			"family_large": False,
			"login_large": True, 
			"failure": False
		}
		template = JINJA_ENVIRONMENT.get_template('templates/login.html')
		self.response.write(template.render(template_values))
	def post(self):
		logging.info("Current path: " + self.request.path)
		username = self.request.get("name")
		password = self.request.get("pw")
		logging.info("Username entered: " + username + ", correct username: Colleen")
		logging.info("Password entered: " + password + ", correct password: pass")
		if username == "Colleen" and password == "pass":
			logging.info("Login success!")
			template_values = {
				"title": "Logged in...",
				"index_large": False,
				"food_large": False,
				"family_large": False,
				"login_large": True,
				"failure": False
			}
			template = JINJA_ENVIRONMENT.get_template('templates/logged_in.html')
			self.response.write(template.render(template_values))
		else:
			logging.info("Login failure!")
			template_values = {
				"title": "Login",
				"index_large": False,
				"food_large": False,
				"family_large": False,
				"login_large": True, 
				"failure": True
			}
			template = JINJA_ENVIRONMENT.get_template('templates/login.html')
			self.response.write(template.render(template_values))
			
app = webapp2.WSGIApplication([
	('/', MainHandler),
    ('/index.html', MainHandler),
    ('/family.html', MainHandler),
    ('/food.html', MainHandler),
	('/login.html', LoginHandler),
	('/logged_in.html', LoginHandler)
], debug=True)