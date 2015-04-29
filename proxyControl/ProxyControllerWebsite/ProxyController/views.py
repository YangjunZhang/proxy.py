# from django.shortcuts import render
from django.http import HttpResponse
from CacheManageCenter import CacheManageCenter
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import os
import httplib


CMC = CacheManageCenter()

# filePath = "ProxyController/files/"
# filePath = "/home/ubuntu/proxy/proxy.py"
# filePath = "/home/ubuntu/proxy/proxy.py/proxyControl/ProxyControllerWebsite/ProxyController/files"
filePath = "None"
centerServer = "None"
centerServerPort = "80"
cacheConf = "ProxyController/cacheCenter.conf"

def hello(request):
	return HttpResponse("hello world, this is proxy controller")


def queryCenter(cacheId):
	if centerServer and centerServer != "None" and centerServer != "none":
		conn = httplib.HTTPConnection(centerServer, int(centerServerPort))
		url = "/ProxyController/query?cacheId=" + cacheId
		method = "GET"
		conn.request(method, url)
		res = conn.getresponse()
		res_data = res.read()
		res.close()
		return res_data
	else:
		return "Cache Miss"

@csrf_exempt
def query(request):
	cacheId = None
	if request.method == 'GET':
		cacheId = request.GET.get('cacheId', None)
	elif request.method == 'POST':
		cacheId = request.POST.get('cacheId', None)
	# if request.
	# return HttpResponse("query Cache Id is:" + cacheId)
	result = "illegal request"
	if cacheId:
		result = CMC.queryCacheID( cacheId)
		if result == None :
			result = queryCenter(cacheId)
			if "Cache Miss" not in result:
				tag = "query result<br>"
				itms = result.split(tag)
				tagsplit = " | "
				keys = itms[1].split(tagsplit)
				# print keys
				cacheId = keys[0]
				server = keys[1]
				port = keys[2]
				reqcnt = keys[3]
				filesize = keys[4]
				CMC.addEntry(CMC.cachedTab, cacheId, server, port, reqcnt, filesize)
				result = itms[1]
				if cacheId in CMC.missTab:
					del CMC.missTab[cacheId]
	if result == None:
		result = "Cache Miss"
	result = "query result<br>" + result
	response = HttpResponse( result )
	response['Content-Length'] = len(result)
	return response

def status( request):
	res = "\n<br>"	
	res = res +"filePath: " + filePath + "\n<br>"
	res = res +"centerServer: " + centerServer + "\n<br>"
	res = res + "centerServerPort: "+centerServerPort + "\n<br>"
	res = res + "cacheConf: "+ cacheConf + "\n<br>"
	return HttpResponse( CMC.serialize()+res)	


def filelist( request):
	if filePath == None or filePath == "None" or filePath == "none":
		return HttpResponse( "Not set file path")
	flist = os.listdir(filePath)
	result = "file list:<br>"
	for itm in flist:
		result =result + itm + " <br>"
	return HttpResponse( result)


def setting(request):
	print "check over1"
	global filePath, centerServer, centerServerPort, cacheConf
	_filePath = None
	_centerServer = None
	_centerServerPort = None
	_cacheConf = None
	if request.method == 'GET':
		_filePath = request.GET.get('filePath', None)
		_centerServer = request.GET.get('centerServer', None)
		_centerServerPort = request.GET.get('centerServerPort', None)
		_cacheConf = request.GET.get('cacheConf', None)
	elif request.method == 'POST':
		_filePath = request.POST.get('filePath', None)
		_centerServer = request.POST.get('centerServer', None)
		_centerServerPort = request.POST.get('centerServerPort', None)
		_cacheConf = request.POST.get('cacheConf', None)
	# print "check over"
	res = ""
	if _filePath:
		filePath = _filePath
	res = res +"filePath: " + filePath + "\n<br>"
	
	if _centerServer:
		centerServer = _centerServer
	res = res +"centerServer: " + centerServer + "\n<br>"
	
	if _centerServerPort:
		centerServerPort = _centerServerPort
	res = res + "centerServerPort: "+centerServerPort + "\n<br>"
	
	if _cacheConf:
		cacheConf = _cacheConf
		CMC.loadConfig(cacheConf)
	res = res + "cacheConf: "+ cacheConf + "\n<br>"

	return HttpResponse(res)

import mimetypes
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper

def download( request):
	if filePath == None or filePath == "None" or filePath == "none":
		return HttpResponse( "Not set file path")

	cacheId = None
	if request.method == 'GET':
		cacheId = request.GET.get('cacheId', None)
	elif request.method == 'POST':
		cacheId = request.POST.get('cacheId', None)

	try:
		# ff = open(filePath+cacheId,"r")
		# generate the file
		chunk_size = 8192
		file_name = filePath +"/"+ cacheId
		response = StreamingHttpResponse(FileWrapper(open( file_name), chunk_size), content_type=mimetypes.guess_type(file_name)[0])
		response['Content-Length'] = os.path.getsize(file_name) 
		response['Content-Disposition'] = "attachment; filename=%s" % cacheId
		# print "before sending"
		return response
		# return HttpResponse( "File does exist!")
	except Exception as e:
		print e
		return HttpResponse( "File does not exist!")