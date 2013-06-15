# -*- coding: utf-8 -*-
from django.template import Template, Context, loader, RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
import datetime

def login_proc(request):
	if request.user.is_authenticated():
		return {
			"authenticated":True, 
			"username":request.user,
			}
	else:
		return {}

def index(request):
	c = Context({"page_title": "浙哪儿欢迎你~"})
	return render_to_response('ZheNar/index.html',c,context_instance = RequestContext(request,processors=[login_proc]))

def getCordinate(request, xx, yy):
	return HttpResponse("info: " + xx + "##" + yy)

    
