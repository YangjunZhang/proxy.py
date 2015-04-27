# from django.shortcuts import render
from django.http import HttpResponse
from CacheManageCenter import CacheManageCenter
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import os

CMC = CacheManageCenter()

def hello(request):
	return HttpResponse("hello world, this is proxy controller")


@csrf_exempt
def query(request):
	cacheId = None
	if request.method == 'GET':
		cacheId = request.GET.get('queryCacheId', None)
	elif request.method == 'POST':
		cacheId = request.POST.get('queryCacheId', None)
	# if request.
	# return HttpResponse("query Cache Id is:" + cacheId)
	result = "illegal request"
	if cacheId:
		result = CMC.queryCacheID( cacheId)
	return HttpResponse( result )

def status( request):
	return HttpResponse( CMC.serialize())	


def files( request):
	filelist = os.listdir("ProxyController/files")
	result = "file list:<br>"
	for itm in filelist:
		result =result + itm + " <br>"
	return HttpResponse( result)

