#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TableEntry(object):

	"""docstring for tableEntry"""

	def __init__(
		self,
		cacheID,
		server,
		port,
		requestCnt,
		fileSize,
		):
		# super(cacedEntry, self).__init__()

		# self.arg = arg

		self.cacheID = cacheID
		self.server = server
		self.port = port
		self.requestCnt = requestCnt
		self.fileSize = fileSize





class CacheManage(object):

	"""docstring for CacheManage"""

	def __init__(self):

		# super(CacheManage, self).__init__()
		# self.arg = arg

		self.cachedTab = {}
		self.missTab = {}

		self.addEntry(self.cachedTab, "a.txt", "127.0.0.1", 8081, 0, 1024)
		self.addEntry(self.missTab, "nocache.txt", None, None, 0, 1024)


	def addEntry(self, table, cacheID, server, port, requestCnt, fileSize):
		te = TableEntry(cacheID, server, port, requestCnt, fileSize)
		table[cacheID] = te

	

	def queryCacheID(self, cacheID):

		# find where to request
		if cacheID in self.cachedTab:
			self.cachedTab[cacheID].requestCnt = self.cachedTab[cacheID].requestCnt + 1
			return self.cachedTab[cacheID].server, self.cachedTab[cacheID].port
		else:
			if cacheID in self.missTab:
				self.missTab[cacheID].requestCnt = self.missTab[cacheID].requestCnt + 1
			else:
				self.addEntry(self.missTab, cacheID, None, None, 1, 0) 
				#update the filesize in miss table  ??
		
		return None, None

	def parseURLKey(self, path):
		# key = None
		if path == "/a.txt":
			return "a.txt"
		return None

	def cacheLookUp(self, clientAddr, url):
		print "##clientAddr: ", clientAddr, " url:", url
		key = self.parseURLKey(url.path)
		host , port = queryCacheID( key)
		# host, port, url
		return host, port, key



	def downloadCache():
		pass


	def __str__(self):
		return 'this is CacheManage'

	def info(self):
		return self.__str__()
