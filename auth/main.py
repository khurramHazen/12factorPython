import argparse
import glog as log
import tornado.web
import tornado.ioloop

from health.health import HealthStatusHandler, HealthUpdateHandler, ReadinessStatusHandler, ReadinessUpdateHandler
from handlers.hello import HelloHandler
from handlers.version import VersionHandler, versionResponse
from handlers.login import LoginHandler
from handlers.jwt_auth import JWTAuthHandler

'''
First you'll need to parse input arguments from command line
'''
parser = argparse.ArgumentParser()
parser.add_argument("--http", default=8880, type=int, help="HTTP service address.")
parser.add_argument("--health", default=8881, type=int, help="Health service address.")
parser.add_argument("--secret", default="secret", help="JWT signing secret.")
args = parser.parse_args()

httpAddr = args.http
healthAddr = args.health
secret = args.secret


'''
You'd log events continously. 
It is not an option rather a must.
'''
log.setLevel("INFO")
log.info("Starting Auth service...")
log.info("Health service listening on %d", healthAddr)
log.info("HTTP service listening on %d", httpAddr)


'''
You'll need a web server.
You'll also need to register entry points with functions/classes.
First you'll register the health services.
Then you'll register the functional services.
'''
check_health_app = tornado.web.Application([
	(r"/healthz", HealthStatusHandler),
	(r"/readiness", ReadinessStatusHandler),
	(r"/healthz/status", HealthUpdateHandler),
	(r"/readiness/status", ReadinessUpdateHandler)
	])

versionResponse.setVersion("1.0.0")

functional_app = tornado.web.Application([
	(r"/login", LoginHandler),
	(r"/version", VersionHandler)
	])

'''
You'll need to run this application
First you'll register the health application with its port.
Then you'll register the functional application with its seperate port.
'''
if __name__ == '__main__':
	check_health_app.listen(healthAddr)
	functional_app.listen(httpAddr)
	tornado.ioloop.IOLoop.current().start()

