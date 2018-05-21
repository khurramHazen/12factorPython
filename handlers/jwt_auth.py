import tornado.web as web

import json
import status
import jwt

from handlers.logging import log_this_request

'''
NEWER
You'll take a JWT token as input and will check if the token is valid, 
	if yes then you'll authorize the user
	otherwise you'll reject the access to user
	An interesting resource/tutorial on JWT is available at 
	https://blog.apcelent.com/json-web-token-tutorial-with-example-in-python.html

You've gotten inspiration for this function from:
	https://github.com/vsouza/JWT-Tornado/blob/master/auth.py

TODO: You'll notice that 'secret_key' is hardcoded.
'''

secret_key = 'secret'
options = { 'verify_signature':	True,
				  'verify_exp': True,
				  'verify_nbf': True,
				  'verify_iat': True,
				  'verify_aud': True
		  }

def not_authorized_reply(in_handler, human_readable_reason_msg):
	in_handler.set_status(status.HTTP_401_UNAUTHORIZED)
	in_handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
	in_handler._transforms = []
	in_handler.write(human_readable_reason_msg)
	in_handler.finish()

def require_jwt_auth(handler_class):

	def wrap_execute(handler_execute):
		def require_auth(handler, kwargs):

			username_header = handler.request.headers.get('Username')
			
			if username_header is None or not username_header.startswith('username '):
				not_authorized_reply(handler, 'Username not provided with token')
				return False

			username = username_header[9:]

			auth_header = handler.request.headers.get('Authorization')
			
			if auth_header:
				parts = auth_header.split()
	
				if parts[0].lower() != 'bearer':
					not_authorized_reply(handler, "Invalid header authorization")
					return False

				elif len(parts) == 1:
					not_authorized_reply(handler, "Invalid header authorization")
					return False

				elif len(parts) > 2:
					not_authorized_reply(handler, "Invalid header authorization")
					return False

				token = parts[1]

				try:
					decoded_token = jwt.decode(token, secret_key, options=options, audience=username)
				except Exception as e:
					not_authorized_reply(handler, str(e))
					return False

			else:
				not_authorized_reply(handler, "Missing authorization")
				return False

			return True

		def _execute(self, transforms, *args, **kwargs):

			try:
				require_auth(self, kwargs)
			except Exception:
				return False

			return handler_execute(self, transforms, *args, **kwargs)

		return _execute

	handler_class._execute = wrap_execute(handler_class._execute)
	return handler_class




@require_jwt_auth
@log_this_request
class JWTAuthHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	def get(self):
		response = "Your JWT certificate is valid."
		
		self.set_status(status.HTTP_200_OK)
		self.write(response)



