import tornado.web as web
import status

from threading import Lock

from handlers.logging import log_this_request


'''
You'll need a service that you can ping conitnously to know if the bigger package is working or not.
You understood correctly, this service will be a part of some bigger package.
You'll implement health and readiness setter getters; setters are required to 
	intentionally introduce 'Service Down'
You'll secure the status variables with lock, as you are not sure how many 
	processes will be simultaneously reading+writing its state.
Then you'll need to expose this functionality to HTTP GET methods.

'''

class health():
	def __init__(self):
		self.healthStatus = status.HTTP_200_OK
		self.readinessStatus = status.HTTP_200_OK
		self.lock = Lock()

	def getHealthStatus(self):
		with self.lock:
			return self.healthStatus

	def getReadinessStatus(self):
		with self.lock:
			return self.readinessStatus

	def setHealthStatus(self, in_status):
		with self.lock:
			self.healthStatus = in_status

	def setReadinessStatus(self, in_status):
		with self.lock:
			self.readinessStatus = in_status


healthz = health()

@log_this_request
class HealthStatusHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	def get(self):
		self.set_status(healthz.getHealthStatus())
		self.write("Health Status\n")

@log_this_request
class HealthUpdateHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	def get(self):
		if healthz.getHealthStatus() == status.HTTP_200_OK:
			healthz.setHealthStatus(status.HTTP_503_SERVICE_UNAVAILABLE)

		elif healthz.getHealthStatus() == status.HTTP_503_SERVICE_UNAVAILABLE:
			healthz.setHealthStatus(status.HTTP_200_OK)

		self.write("Updated Health Status\n")

@log_this_request
class ReadinessStatusHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	def get(self):
		self.set_status(healthz.getReadinessStatus())
		self.write("Readiness Status\n")

@log_this_request
class ReadinessUpdateHandler(web.RequestHandler):
	SUPPORTED_METHODS = ("GET")

	def get(self):
		if healthz.getReadinessStatus() == status.HTTP_200_OK:
			healthz.setReadinessStatus(status.HTTP_503_SERVICE_UNAVAILABLE)
			
		elif healthz.getReadinessStatus() == status.HTTP_503_SERVICE_UNAVAILABLE:
			healthz.setReadinessStatus(status.HTTP_200_OK)

		self.write("Updated Readiness Status\n")





