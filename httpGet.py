#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import urllib


def main():
	print 'hello'
	httpClient = None
	try:
		params = urllib.urlencode({'queryCacheId': 'a.txt'})
		headers = {'Content-type': 'application/x-www-form-urlencoded',
             'Accept': 'text/plain'}
		server = '192.168.3.110'
		port = 28000
		httpClient = httplib.HTTPConnection(server, port, timeout=30)
		# httpClient.request('POST', 'ProxyController/query/', params, headers)
		httpClient.request('GET', 'ProxyController/query/?queryCacheId=a.txt')
		response = httpClient.getresponse()
		print response.status
		print response.reason
		print response.read()
		print response.getheaders()
	except Exception, e:
		print e
	finally:
		if httpClient:
			httpClient.close()


if __name__ == '__main__':
	main()
