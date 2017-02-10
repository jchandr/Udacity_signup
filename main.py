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
import os
import jinja2
import webapp2
import re

template_dir = os.path.join(os.path.dirname(__file__))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))

class MainHandler(Handler):
    def get(self):
        self.render("signup_page.html")

    def post(self):
    	username = self.request.get("username")
    	email = self.request.get("email")
    	password = self.request.get("password")
    	password_verify = self.request.get("password_verify")
    	check_credentials = "check credentials"
       	if(not(validate_username(username) and validate_password(password,password_verify) and validate_email(email))):
       		self.render("signup_page.html",check_credentials=check_credentials)
       	else:
       		self.render('welcome.html',username=username)


def validate_email(email):
	if(email == ""):
		return True
	email_regex = "^[\S]+@[\S]+.[\S]+$"
	email_validator = re.search(email_regex, email, re.M|re.I)
	if(email_validator):
		return True
	else:
		return False

def validate_username(u):
	username_regex = "^[a-zA-Z0-9_-]{3,20}$"
	username_validator = re.search(username_regex, u, re.M|re.I)
	if(username_validator):
		return True
	else:
		return False

def validate_password(p,p_v):
	password_regex = "^.{3,20}"
	if(str(p_v) == str(p)):
		password_validator = re.search(password_regex, p, re.M|re.I)
		if(password_validator):
			return True
		else:
			return False
	else:
		return False


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
