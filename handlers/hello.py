import tornado.web as web

import json
import status

from handlers.logging import log_this_request

'''
You'll need a dummy page, like Hello World!, which you can return on a HTTP GET request
'''

@log_this_request
class HelloHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	def get(self):
		data = {}
		data['Message'] = "Hello"
		response_json = json.dumps(data)

		self.set_status(status.HTTP_200_OK)
		self.write(response_json)

