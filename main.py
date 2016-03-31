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
import hashlib
import uuid

# Lets set it up so we know where we stored the template files
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
# holds username/password
login_data = {}
	

class MainHandler(webapp2.RequestHandler):
    def get(self):
		current_page = self.request.path
		logging.info("Current path: " + current_page)
		title = ""
		index_large = False
		food_large = False
		family_large = False
		if "work" in current_page:
			title = "Work"
		elif "interests" in current_page:
			title = "Interests"
		elif "skills" in current_page:
			title = "skills"
		else:
			current_page += "index"
			title = "Home"
		template_values = {
			"title": title,
		}
		template = JINJA_ENVIRONMENT.get_template('templates' + current_page + '.html')
		self.response.write(template.render(template_values))

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/login.html')
		self.response.write(template.render())
	def post(self):
		status = "False"
		username = self.request.get("name")
		if username in login_data:
			status = "True"
		logging.info('username in dict: ' + status)		
		password = self.request.get("pw")
		if username not in login_data:
			template_values = {
				"error_message": "Username does not exist"
			}
			template = JINJA_ENVIRONMENT.get_template('templates/login.html')
			self.response.write(template.render(template_values))
			
		# if username == "Colleen" and password == "pass":
			# logging.info("Login success!")
			# template_values = {
				# "title": "Logged in...",
				# "index_large": False,
				# "food_large": False,
				# "family_large": False,
				# "login_large": True,
				# "failure": False
			# }
			# template = JINJA_ENVIRONMENT.get_template('templates/logged_in.html')
			# self.response.write(template.render(template_values))
		# else:
			# logging.info("Login failure!")
			# template_values = {
				# "title": "Login",
				# "index_large": False,
				# "food_large": False,
				# "family_large": False,
				# "login_large": True, 
				# "failure": True
			# }
			# template = JINJA_ENVIRONMENT.get_template('templates/login.html')
			# self.response.write(template.render(template_values))
		
def add_user(username, password):
	algorithm = 'sha512'
	salt = uuid.uuid4().hex
	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash = m.hexdigest()
	result = "$".join([algorithm, salt, password_hash])
	login_data[username] = result
		
class NewUserHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {
			"get": True
		}
		template = JINJA_ENVIRONMENT.get_template('templates/user.html')
		self.response.write(template.render(template_values))
	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		# username already taken, not available
		if username in login_data:
			template_values = {
				"get": False,
				"success": False
			}
			template = JINJA_ENVIRONMENT.get_template('templates/user.html')
			self.response.write(template.render(template_values))
		# username not already taken
		else:
			logging.info("username not taken")
			template_values = {
				"success": True
			}
			add_user(username, password)
			template = JINJA_ENVIRONMENT.get_template('templates/user.html')
			self.response.write(template.render(template_values))
			
class EditUserHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/edit_user.html')
		self.response.write(template.render())
	def post(self):
		template = JINJA_ENVIRONMENT.get_template('templates/edit_user.html')
		self.response.write(template.render())
			
app = webapp2.WSGIApplication([
	('/', MainHandler),
    ('/work', MainHandler),
    ('/interests', MainHandler),
    ('/skills', MainHandler),
	('/user', NewUserHandler),
	('/edit_user', EditUserHandler),
	('/login', LoginHandler),
	('/logout', LoginHandler)
], debug=True)