# encoding: UTF-8
''' Main View '''
import sys
import classroomUtil # 数据库操作模块
import settings
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta

reload(sys)
sys.setdefaultencoding('utf8')

# 首页
def index(request):
	return render_to_response('query.html')

# 方便记忆的链接
def shortIndex(request):
	return HttpResponseRedirect('/queryEmptyClassrooms/index/')

# 关于
def about(request):
	return render_to_response('about.html')

# 响应查询空教室
def queryEmptyClassrooms(request):
	try:
		classWeek = int(request.GET['classWeek']) # 星期几
		classWeekNum = int(request.GET['classWeekNum']) # 第几周
		beginTime = int(request.GET['beginTime']) # 开始时间
		endTime = int(request.GET['endTime']) # 结束时间
		if not ((1 <= classWeekNum <= 20) \
			and (1 <= classWeek <= 7) \
			and (1 <= beginTime <= 13) \
			and (1 <= endTime <= 13)
			and (beginTime <= endTime)):
			return HttpResponse(json.dumps("", ensure_ascii = False))
	except:
		return HttpResponse(json.dumps("", ensure_ascii = False))

	classrooms = classroomUtil.getEmptyClassrooms(classWeek, classWeekNum, beginTime, endTime)
	return HttpResponse(json.dumps(classrooms, ensure_ascii = False))

# 指定【校区，第几周，周几，开始，结束】的API
def queryCommonAPI(request, location, classWeekNum, classWeek, beginTime, endTime):
	try:
		cwn = int(classWeekNum)
		cw = int(classWeek)
		bt = int(beginTime)
		et = int(endTime)
		if not ((1 <= cwn <= 20) \
			and (1 <= cw <= 7) \
			and (1 <= bt <= 13) \
			and (1 <= et <= 13)
			and (bt <= et)):
			return HttpResponse(json.dumps("", ensure_ascii = False))
	except:
		return HttpResponse(json.dumps("", ensure_ascii = False))

	if location == 'djq':
		return HttpResponse(
			json.dumps(classroomUtil.getDJQ(classWeek, classWeekNum, beginTime, endTime), 
				ensure_ascii = False))


	classrooms = classroomUtil.getEmptyClassrooms(cw, cwn, bt, et)

	# 根据校区返回
	if location == 'spl':
		return HttpResponse(json.dumps(classrooms['SPL'], ensure_ascii = False))
	elif location == 'jlh':
		return HttpResponse(json.dumps(classrooms['JLH'], ensure_ascii = False))
	elif location == 'djq':
		return HttpResponse(json.dumps(classrooms['DJQ'], ensure_ascii = False))
	elif location == 'all':
		return HttpResponse(json.dumps(classrooms, ensure_ascii = False))


# 指定【校区，今天（明天），开始，结束】的API
def querySpecifiedAPI(request, location, askDate, beginTime, endTime):
	# 检查所传参数的合法性
	try:
		beginTime = int(beginTime)
		endTime = int(endTime)
		if not ((1 <= beginTime <= 13) \
			and (1 <= endTime <= 13) \
			and (beginTime <= endTime)):
			return HttpResponse(json.dumps("", ensure_ascii = False))
	except:
		return HttpResponse(json.dumps("", ensure_ascii = False))

	# 13-14-3学期第一周周一的日期
	START_YEAR = settings.START_YEAR
	START_MONTH = settings.START_MONTH
	START_DAY = settings.START_DAY

	# 计算参数
	startDate = date(START_YEAR, START_MONTH, START_DAY)
	checkDate = date.today()
	if askDate == 'tomorrow': # 明天
		try:
			checkDate = date(checkDate.year, checkDate.month, checkDate.day + 1)
		except: # out of day
			try: 
				checkDate = date(checkDate.year, checkDate.month + 1, 1)
			except: # out of month
				checkDate = date(checkDate.year + 1, 1, 1)
	delta = checkDate - startDate # 相差的天数
	classWeekNum = delta.days / 7 + 1 # 第几周
	classWeek = checkDate.isoweekday() # 周几

	if location == 'djq':
		return HttpResponse(
			json.dumps(classroomUtil.getDJQ(classWeek, classWeekNum, beginTime, endTime), 
				ensure_ascii = False))

	classrooms = classroomUtil.getEmptyClassrooms(classWeek, classWeekNum, beginTime, endTime)

	# 根据校区返回
	if location == 'spl':
		return HttpResponse(json.dumps(classrooms['SPL'], ensure_ascii = False))
	elif location == 'jlh':
		return HttpResponse(json.dumps(classrooms['JLH'], ensure_ascii = False))
	elif location == 'djq':
		return HttpResponse(json.dumps(classrooms['DJQ'], ensure_ascii = False))
	elif location == 'all':
		return HttpResponse(json.dumps(classrooms, ensure_ascii = False))


# jQuery-mobile
def mobile(request):
	return render_to_response('index.html')
