# encoding: UTF-8

from django.conf.urls import patterns, include, url
import queryEmptyClassrooms.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # API
    (r'^queryEmptyClassrooms/query/([a-z]{3})/(\d{1,2})/(\d{1,2})/(\d{1,2})/(\d{1,2})/$',
        queryEmptyClassrooms.views.queryCommonAPI), # 指定【校区，第几周，周几，开始，结束】
    (r'^queryEmptyClassrooms/query/([a-z]{3})/([a-z]+)/(\d{1,2})/(\d{1,2})/$', 
        queryEmptyClassrooms.views.querySpecifiedAPI), # 指定【校区，今天（明天），开始，结束】

    # 查询
	(r'^queryEmptyClassrooms/query/$', queryEmptyClassrooms.views.queryEmptyClassrooms), 

    # 首页
	(r'^queryEmptyClassrooms/index/$', queryEmptyClassrooms.views.index),
    (r'^webapp/classroom/$', queryEmptyClassrooms.views.shortIndex), # 方便记忆的链接

    # 关于本站
    (r'^queryEmptyClassrooms/about/$', queryEmptyClassrooms.views.about),
   
    
    # Examples:
    # url(r'^$', 'queryEmptyClassrooms.views.home', name='home'),
    # url(r'^queryEmptyClassrooms/', include('queryEmptyClassrooms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
