import tornado.web as web

import json
import status
import base64
import bcrypt
import datetime
import jwt

from user.users import Users

from handlers.logging import log_this_request


MAX_SESSION_TIME_IN_SECS = 60

'''
You'll need an end-point function/handler that can take username and password as input and check if that
	user is registered with your system. It is called BasicAuthentication.
You'll find a good tutorial on BasicAuthentication with Tornado and Python on the follwoing link:
	http://kevinsayscode.tumblr.com/post/7362319243/easy-basic-http-authentication-with-tornado
'''

def require_basic_auth(handler_class):

	def wrap_execute(handler_execute):

		def require_basic_auth(handler, kwargs):
			auth_header = handler.request.headers.get('Authorization')

			if auth_header is None or not auth_header.startswith('Basic '):
				handler.set_status(status.HTTP_401_UNAUTHORIZED)
				handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
				handler._transforms = []
				handler.finish()
				return False

			auth_decoded = base64.decodestring( bytes(auth_header[6:], 'utf-8') )
			kwargs['basicauth_user'], kwargs['basicauth_pass'] = auth_decoded.split(b':', 2)

			if isinstance(kwargs['basicauth_user'], bytes):
				kwargs['basicauth_user'] = kwargs['basicauth_user'].decode('utf-8')
			
			if kwargs['basicauth_user'] is None or kwargs['basicauth_pass'] == None:
				handler.set_status(status.HTTP_401_UNAUTHORIZED)
				handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
				handler._transforms = []
				response = 'Username or Password is missing'
				handler.write(response)
				handler.finish()
				return False

			'''
			TODO:
			How to check/match username & password with existing database?
			How to get access to database at this stage?
			Shouldn't the database access be not hardcoded here, instead DB's get username&password
				functions handler be here so that its implementation is at one central place (in users.py)
			'''
			if not Users.match_credentials(kwargs['basicauth_user'], kwargs['basicauth_pass']):
				handler.set_status(status.HTTP_401_UNAUTHORIZED)
				handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
				handler._transforms = []
				response = 'Username and Password didn\'t match'
				handler.write(response)
				handler.finish()
				return False
			
			return True

		def _execute(self, transforms, *args, **kwargs):
			if not require_basic_auth(self, kwargs):
				return False
			return handler_execute(self, transforms, *args, **kwargs)

		return _execute

	handler_class._execute = wrap_execute(handler_class._execute)
	return handler_class

'''
You know that the follwoing order of 'wrappers' DOES matter; if these are reversed you'll not be 
	able to log every hit on /login instead only successfully authenticated hits will be logged and
	I am sure you'd not want that as you'll want to know if someone is trying to get into your system
	using brute force.
'''
@log_this_request
@require_basic_auth
class LoginHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	'''
	TODO: Why do you need 'basicauth_user' & 'basicauth_pass' from @require_basic_auth
	'''
	def get(self, basicauth_user, basicauth_pass):
		'''
		You'll generate JWT Token here.
		TODO: You'll notice that 'secret' is hardcoded
		TODO: You'll notice that user entered password is present in plain text in 'basicauth_pass'
		TODO: You'll notice that password is being transmitted from user to server in plain-text
		'''
		token = jwt.encode(
			{
			'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=MAX_SESSION_TIME_IN_SECS),
			'nbf': datetime.datetime.utcnow(),
			'iss': "auth.service",
			'iat': datetime.datetime.utcnow(),
			'aud': basicauth_user
			},
			'secret', 
			algorithm='HS256'
			)

		response =  json.dumps( { 'Token': token.decode('utf-8') } ) #json.dumps(token)
		self.set_status(status.HTTP_200_OK)
		self.write(response)



































