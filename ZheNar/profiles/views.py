# Create your views here.
# <-* encoding=utf8 *->
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from django.views.decorators.http import require_POST, require_GET

from profiles.models import Profile
from places.models import Place
from events.models import Event

import re, random


def index(request):
	return HttpResponse("index!")


def debug(request, info):
	return HttpResponse("debug information: " + info)


@require_POST
def _login(request):
	if request.POST:
		account = request.POST['account']
		password = request.POST['password']
	else:
		return HttpResponseRedirect(reverse('index'))

	upr = authenticate(username=account, password=password)
	if upr is None:
		try:
			upr = User.objects.get(email=account)
			upr = authenticate(username=upr.username, password=password) #check if user logins with email
		except User.DoesNotExist:
			return __goErrorPage(request, ["Wrong account or password", ])

	if upr is None:
		return __goErrorPage(request, ["Wrong account or password", ])
	else :
		if upr.is_active == 0:					#This user has not been active
			return __goErrorPage(request, ["This user have been disactivated", ])
		#if upr.is_superuser == 1:				#Superuser should not login in this page
		#	return __goErrorPage(request, ["Superuser should not login in this page", ])
	
	login(request, upr)		#log in
	return HttpResponseRedirect(reverse('index'))


def _logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def register(request):
	context = {'page_title': "浙哪儿注册喽！", }
	return render(request, 'profiles/register.html', __login_proc(request, context))


@require_POST
def _register(request):
	if request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		name = request.POST.get('name')
		gender = 0
		if request.POST.get('gender') == "1":
			gender = 1
		elif request.POST.get('gender') == "2":
			gender = 2
		registerTime = datetime.now()
	else:
		return HttpResponseRedirect(reverse('index'))

	try:
		upr = User.objects.get(username=username)	#check if there is duplicated username
	except User.DoesNotExist:
		upr = None
	if upr is not None:
		return __goErrorPage(request, ["duplicated username", ])

	try:
		upr = User.objects.get(email=email)		#check if there is duplicated email
	except User.DoesNotExist:
		upr = None
	if upr is not None:	
		return __goErrorPage(request, ["dupicated email!", ])
	
	form = {}
	if __judge_form(form):
		upr = User.objects.create_user(username, email, password)
		pr = Profile(user=upr, name=name, gender=gender, registerTime=registerTime)
		pr.save()
		userpr = authenticate(username=username, password=password)
		login(request, userpr)
	else:
		return __goErrorPage(request, ["something wrong with your form", ])
	
	return HttpResponseRedirect(reverse('index'));


def settings(request):
	if request.user.is_authenticated():
		pr = Profile.objects.get(user_id=request.user.id);
		check1 = "";
		check2 = "";
		if pr.gender == 1:
			check1 = "checked"
		if pr.gender == 2:
			check2 = "checked"
		back_info = request.session.get('back_info')
		context = {
			'page_title': '浙哪儿设置',
			'pr': pr,
			'check1': check1,
			'check2': check2,
			'back_info': back_info,
		}
		request.session['back_info'] = None
		
		return render(request, "profiles/settings.html", __login_proc(request, context))
	else :
		return HttpResponseRedirect(reverse('index'))


def _settings(request):
	if request.user.is_authenticated() and request.POST:
		username = request.user.username
		email = request.user.email
		change_password = request.POST.get('change_password')
		if change_password: 
			password = request.POST.get('password')
			ori_password = request.POST.get('password_ori')
		name = request.POST.get('name')
		gender = request.POST.get('gender')
	else:
		return HttpResponseRedirect(reverse('index'))

	form = {}
	if __judge_form(form):
		upr = request.user
		if change_password == "1":
			upr = authenticate(username=username, password=ori_password) #check if ori_password match the user name
			if upr is None:
				return __goErrorPage(request, ["your original password is not right", ])
			upr.set_password(password)
			upr.save()
		pr = Profile.objects.get(user_id = upr.id)
		pr.name = name
		pr.gender = gender
		pr.save()
	else:
		return __goErrorPage(request, ["something wrong with your form", ])

	
	request.session['back_info'] = "保存成功！"
	return HttpResponseRedirect(reverse('profiles:settings'))


def manage(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))

	place_list_tmp = Place.objects.filter(creater_id = request.user.id)
	place_list = [item for item in place_list_tmp if item.status != 4]
	pr = Profile.objects.get(user_id = request.user.id)
	event_list_tmp = Event.objects.filter(holder_id = pr.id)
	event_list = [item for item in event_list_tmp if item.status != 4]
	
	context = {
			"page_title": "浙哪儿 - 管理你的活动",
			"place_list": place_list,
			"event_list": event_list,
	}
	return render(request, "profiles/manage.html", __login_proc(request, context))


def syncSuperUser(request):
	superuser_list = User.objects.filter(is_superuser = 1)
	for item in superuser_list:
		pr = Profile(user = item, name=item.username)
		pr.save()
	return HttpResponseRedirect(reverse('index'))


def __login_proc(request, lst):
	if request.user.is_authenticated():
		lst['authenticated'] = True;
		lst['username'] = request.user.username
		return lst
	return lst


def __judge_form(form):
	return True


def __goErrorPage(request, error_list):
	return render(request, "error/error_popup.html", __login_proc(request, {'error_list': error_list}))

