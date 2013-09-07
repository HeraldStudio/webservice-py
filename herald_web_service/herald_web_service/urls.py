from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^herald_web_service/$', 'herald_web_service.views.home', name='home'),
    # url(r'^herald_web_service/', include('herald_web_service.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

#curriculum
urlpatterns += patterns('curriculum_service.views',
    url(r'^herald_web_service/curriculum/([\w]+)/([\w-]+)/$', 'parserHtml'),
    url(r'^herald_web_service/curriculum/term/$', 'getCurriculumTerm'),
)


# tyx
urlpatterns += patterns('tyx_service.views',
  url(r'^herald_web_service/tyx/([\w]+)/([\w]+)/$', 'tyxPc'),
)


#jwc
urlpatterns += patterns('jwcInfor.views',
  url(r'^herald_web_service/jwc/$', 'getJwcInfor'),
)


# library
urlpatterns += patterns('seulibrary.views',
    # Examples:
    # url(r'^$', 'libsite.views.home', name='home'),
    # url(r'^libsite/', include('libsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^herald_web_service/library/instruction/$', 'instruction'),
    url(r'^herald_web_service/library/search_book/$', 'search_book'),
    url(r'^herald_web_service/library/book_detail/$', 'book_detail'),
    url(r'^herald_web_service/library/rendered_books/$', 'check_render_books'),
    url(r'^herald_web_service/library/renew/$', 'renew_book'),
    url(r'^herald_web_service/library/appointed_books/$', 'check_appointed_books'),
    url(r'^herald_web_service/library/appoint_book/$', 'appoint_book'),
    url(r'^herald_web_service/library/cancel_appoint/$', 'cancel_appoint'),
    url(r'^herald_web_service/library/appoint_info/$', 'appoint_info'),
    url(r'^herald_web_service/library/appoint_book/$', 'appoint_book'),
)




