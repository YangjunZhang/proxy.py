#!/usr/bin/env python
# -*- coding: utf-8 -*-

TableEntrySize = 5


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

	def __str__(self):
		tag = '    '
		return self.cacheID + tag + self.server + tag + str(self.port) + tag \
   + str(self.requestCnt) + tag + str(self.fileSize)


class CacheManage(object):

	"""docstring for CacheManage"""

	def __init__(self):

		# super(CacheManage, self).__init__()
		# self.arg = arg

		self.cachedTab = {}
		self.missTab = {}
		self.urlMatchKeyArr = []  # regex

		# self.addEntry(self.cachedTab, "a.txt", "127.0.0.1", 8081, 0, 1024)
		# self.addEntry(self.missTab, "nocache.txt", None, None, 0, 1024)

		self.cachedTab_key = '## CachedTable ##'
		self.missTab_key = '## MissTable ##'
		self.urlMatch_key = '## UrlMatchKey ##'

		# self.tag     = '\t'

		self.tag = '    '

	def addEntry(
		self,
		table,
		cacheID,
		server,
		port,
		requestCnt,
		fileSize,
		):
		te = TableEntry(cacheID, server, port, requestCnt, fileSize)
		table[cacheID] = te

	def queryCacheID(self, cacheID):

		# find where to request

		if cacheID in self.cachedTab:
			self.cachedTab[cacheID].requestCnt = self.cachedTab[cacheID].requestCnt + 1
			return (self.cachedTab[cacheID].server, self.cachedTab[cacheID].port)
		else:
			if cacheID in self.missTab:
				self.missTab[cacheID].requestCnt = self.missTab[cacheID].requestCnt + 1
			else:
				self.addEntry(
					self.missTab,
					cacheID,
					None,
					None,
					1,
					0,
					)

				# update the filesize in miss table  ??

		return (None, None)

	def parseURLKey(self, path):

		# key = None

		if path == '/a.txt':
			return 'a.txt'
		return None

	def cacheLookUp(self, clientAddr, url):
		print '##clientAddr: ', clientAddr, ' url:', url
		key = self.parseURLKey(url.path)
		(host, port) = queryCacheID(key)

		# host, port, url

		return (host, port, key)

	def loadConfig(self, fileName):
		try:

			filein = open(fileName, 'r')
			self.cacheConfigFile = fileName
			line = filein.readline()

			if self.cachedTab_key in line:
				line = filein.readline()
				while line != '' and self.missTab_key not in line:
					line = line[0:len(line) - 1]
					itms = line.split(self.tag)
					# print itms
					if len(itms) == TableEntrySize:
						self.addEntry(
							self.cachedTab,
							itms[0],
							itms[1],
							int(itms[2]),
							int(itms[3]),
							int(itms[4]),
							)
					line = filein.readline()

			if self.missTab_key in line:
				line = filein.readline()
				while line != '' and self.urlMatch_key not in line:
					line = line[0:len(line) - 1]
					itms = line.split(self.tag)
					if len(itms) == TableEntrySize:
						self.addEntry(
							self.missTab,
							itms[0],
							itms[1],
							int(itms[2]),
							int(itms[3]),
							int(itms[4]),
							)
					line = filein.readline()

			if self.urlMatch_key in line:
				line = filein.readline()
				while line != '':
					line = line[0:len(line) - 1]
					itms = line.split(self.tag)
					# print itms
					if itms[0] == 'regex':
						self.urlMatchKeyArr.append(itms[1])
					line = filein.readline()
			
			print self.cachedTab_key
			print self.cachedTab
			print self.missTab_key
			print self.missTab
			print self.urlMatch_key
			print self.urlMatchKeyArr
			filein.close()

			return True
		except IOError:
			print 'Error: File ' + fileName + ' does not appear to exist.'
		return False

	def saveConfig(self):

		fileout = open(self.cacheConfigFile, 'w')
		print >> fileout, self.cachedTab_key
		for key in self.cachedTab:
			print >> fileout, self.cachedTab[key].__str__()
		print >> fileout

		print >> fileout, self.missTab_key
		for key in self.missTab:
			print >> fileout, self.missTab[key].__str__()
		print >> fileout

		print >> fileout, self.urlMatch_key
		for itm in self.urlMatchKeyArr:
			print >> fileout, 'regex'+ self.tag + itm
		print >> fileout
		
		fileout.close()
		print "configure file out"

	def downloadCache():
		pass

	def __str__(self):
		return 'this is CacheManage'

	def info(self):
		return self.__str__()
