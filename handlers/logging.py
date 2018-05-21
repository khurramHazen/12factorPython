import tornado.web as web

from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


'''
You've taken datetime representation in RFC 1123 format from:
	https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python
'''

# class LoggingHandler(web.RequestHandler):
# 	SUPPORTED_METHODS = ("GET")

# 	def get(self):

# 		remote_ip = self.request.remote_ip
# 		now_time = format_date_time( mktime( datetime.utcnow().timetuple() ) )
# 		method = self.request.method
# 		uri = self.request.uri
# 		protocol = self.request.protocol
# 		user_agent = self.request.headers["User-Agent"]

# 		log_string = '{} - - [{}] \"{} {} {}\" {}\n'.format(remote_ip, now_time, method, uri, protocol, user_agent)
		
		
# 		self.set_status(status.HTTP_200_OK)
# 		self.write(log_string)


def log_this_request(handler_class):

	def wrap_execute(handler_execute):
		def do_logging(handler, kwargs):

			remote_ip = handler.request.remote_ip
			now_time = format_date_time( mktime( datetime.utcnow().timetuple() ) )
			method = handler.request.method
			uri = handler.request.uri
			protocol = handler.request.protocol
			user_agent = handler.request.headers["User-Agent"]

			log_string = '{} - - [{}] \"{} {} {}\" {}\n'.format(remote_ip, now_time, method, uri, protocol, user_agent)
			
			print(log_string)
			

		def _execute(self, transforms, *args, **kwargs):

			try:
				do_logging(self, kwargs)
			except Exception:
				return False
				
			return handler_execute(self, transforms, *args, **kwargs)

		return _execute

	handler_class._execute = wrap_execute(handler_class._execute)
	return handler_class