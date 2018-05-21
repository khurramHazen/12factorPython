import tornado.web as web

import json
import status

from handlers.logging import log_this_request


'''
You'll need a function handler that will return the code version to a calling function
You'll implement it as a web request handler 
You'll also need a class-object that can set-get the version between calls as you'd not want to make
	it static/fixed.
'''

class VersionResponse():
	def __init__(self):
		self.version = None
	def setVersion(self, in_version):
		self.version = in_version
	def getVersion(self):
		return self.version

versionResponse = VersionResponse()

@log_this_request
class VersionHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	def get(self):
		data = {}
		data['Version'] = versionResponse.getVersion()
		response_json = json.dumps(data)

		self.set_status(status.HTTP_200_OK)
		self.write(response_json)

