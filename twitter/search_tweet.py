 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import json
import httplib
import base64
import string
import urllib


username = "your_user_name"
password = "your_password"


def search_twitter(params):
	auth = 'Basic ' + string.strip(base64.encodestring(username + ":" + password))
	url = "pcred.yonsei.ac.kr"
	# url += "?query=" + query
	print url
	port = 5000
	conn = httplib.HTTPConnection(url, port)

	url_values = urllib.urlencode(params)	
	conn.putrequest("GET", "/twitter?" + url_values)
	conn.putheader("Authorization", auth)	
	conn.endheaders()

	
	res = conn.getresponse()
	print res.status, res.reason, res.read()



def test_twitter():
	params = dict()
	params["query"]	= "무한도전"
	search_twitter(params)

def main():
	test_twitter()

if __name__ == "__main__":
	main()
