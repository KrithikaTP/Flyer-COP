import urllib, urllib2, time
from datetime import datetime
import random

REST_API_URL = "YOUR POWERBI API URL"


def sendDataToPowerBi(person,min_distance,signal_count,social_dist_violators,two_wheeler_count,four_wheeler_count,objects):
	try:
		now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")

		data = '[{{ "time": "{0}", "signal_count": "{1}","social_dist_violator": "{2}","min_distance": "{3}","two_wheel": "{4}","four_wheel": "{5}","person": "{6}"' + str(objects) +'}}]'.format(now,signal_count,social_dist_violators,min_distance,two_wheeler_count,four_wheeler_count,person)

		# make HTTP POST request to Power BI REST API
		req = urllib2.Request(REST_API_URL, data)
		response = urllib2.urlopen(req)
		print("POST request to Power BI with data:{0}".format(data))
		print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))

		time.sleep(10)
	except urllib2.HTTPError as e:
		print("HTTP Error: {0} - {1}".format(e.code, e.reason))
	except urllib2.URLError as e:
		print("URL Error: {0}".format(e.reason))
	except Exception as e:
		print("General Exception: {0}".format(e))
