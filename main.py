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
from webapp2_extras import sessions
import os
import logging
import jinja2
import hashlib
import uuid
import csv

# Lets set it up so we know where we stored the template files
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
# holds username/password
login_data = {}
	
# returns dictionary indexed by username
# values are tuples of (hash, salt, hashed & salted password)
def get_login_data():
	data = open('login_credentials.csv', 'r')
	reader = csv.reader(data, delimiter=',')
	login_data = {}
	for row in reader:
		# login_data[username] = (hash, salt, hashed/salted pwd)
		login_data[row[0]] = (row[1], row[2], row[3])
	return login_data

# returns true if password matches
def check_pwd(username, pwd, login_data):
	password = login_data[username][2]
	salt = login_data[username][1]
	hash = login_data[username][0]
	m = hashlib.new(hash)
	m.update(salt + pwd)
	pwd_hash = m.hexdigest()
	# if hashed passwords don't match
	if pwd_hash != password:
		return False
	return True

def write_file(login_data):
	f = open('login_credentials.csv', 'w')
	for name in login_data:
		f.write(name + ',' + str(login_data[name][0]) + ',' + str(login_data[name][1]) + ',' + str(login_data[name][2]))
	return
	
# taken from https://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '2D07169pH4DV998p885NCo4iYEgys1CJ',
}

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
	
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
		login_data = get_login_data()
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
		else:
			self.session['username'] = username;
			if check_pwd(username, password, login_data) == True:
				template_values = {
					name = self.session['username']
				}
				template = JINJA_ENVIRONMENT.get_template('templates/logged_in.html')
				self.response.write(template.render())
			else:
				template_values = {
					"error_message": "Username and password do not match"
				}
				template = JINJA_ENVIRONMENT.get_template('templates/login.html')
				self.response.write(template.render(template_values))
		
def add_user(username, password, login_data):
	algorithm = 'sha512'
	salt = uuid.uuid4().hex
	m = hashlib.new(algorithm)
	m.update(salt + password)
	password_hash = m.hexdigest()
	login_data[username] = (algorithm, salt, password_hash)
	f = open('login_credentials.csv', 'a')
	f.write(str(username) + ',' + str(algorithm) + ',' + str(salt) + ',' + str(password_hash))
	
def edit_user(username, old_password, new_password, login_data):
	status = check_pwd(username, old_password, login_data)
	if not status:	# if incorrect old password
		return False
	else:			# correct old password
		salt = login_data[username][1]
		hash = login_data[username][0]
		m = hashlib.new(hash)
		m.update(salt + new_password)
		pwd_hash = m.hexdigest()
		login_data[username] = (hash, salt, pwd_hash)
		write_file(login_data)
		return True
		
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
		login_data = get_login_data()
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
		login_data = get_login_data()
		username = self.session['username']
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
], debug=True, config=config)