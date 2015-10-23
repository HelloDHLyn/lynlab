# -*- coding: utf-8 -*-

"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.http import HttpResponse

from blog.views import PostList, PostDetail, PostCreate
#from wiki.views import WikiHome, WikiContent

urlpatterns = patterns('',
                       # blog:
                       url(r'^$', RedirectView.as_view(url='blog/')),
                       url(r'^blog/$', PostList.as_view(), name='home'),
                       url(r'^blog/(?P<pk>\d+)/$', PostDetail.as_view(), name='detail'),
                       url(r'^blog/create/$', PostCreate.as_view(), name='create'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       # wiki:
                       #url(r'^wiki/$', WikiHome.as_view(), name='wiki'),
                       #url(r'^wiki/view/$', WikiContent.as_view(), name='wikicontent'),

                       # admin:
                       url(r'^admin/', include(admin.site.urls)),

                       # member:
                       url(r'^login/$', 'django.contrib.auth.views.login'),

                       # static:
                       url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
                       )