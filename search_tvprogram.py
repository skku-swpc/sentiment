 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import json
import httplib
import base64
import string
import urllib

username = "your_user_name"
password = "your_password"

def search_program(params):
  auth = 'Basic ' + string.strip(base64.encodestring(username + ":" + password))
	url = "pcred.yonsei.ac.kr"
	# url += "?query=" + query
	print url
	port = 5000
	conn = httplib.HTTPConnection(url, port)

	url_values = urllib.urlencode(params)	
	conn.putrequest("GET", "/program?" + url_values)
	conn.putheader("Authorization", auth)	
	conn.endheaders()

	
	res = conn.getresponse()
	print res.status, res.reason, res.read()


def test_search():
	params = dict()
	params["title"] = ""
	params["days"] = ""
	params["onair"] = ""
	params["ch"] = ""
	params["casts"] = "유재석,박명수"
	search_program(params)
	

def main():
  test_search()

if __name__ == "__main__":
	main()

	
	
