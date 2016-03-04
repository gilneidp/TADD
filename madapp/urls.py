"""madapp URL Configuration

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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

# ... the rest of your URLconf goes here ...

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login),
    url(r'^$', 'madapp.mad.views.index'),
    url(r'^home/$', 'madapp.mad.views.index'),
    #url(r'^config/$', include(admin.site.urls)),
    url(r'^about/$', 'madapp.mad.views.about'),
    url(r'^honeypotstatus/$', 'madapp.mad.views.honeypotstatus'),
    url(r'^poxstatus/$', 'madapp.mad.views.poxstatus'),
    url(r'^tempflows/$', 'madapp.mad.views.tempflows'),
    url(r'^installedflows/$', 'madapp.mad.views.installedflows'),
    url(r'^poxlogs/$', 'madapp.mad.views.poxlogs'),
    url(r'^rules/$', 'madapp.mad.views.rules'),
    url(r'^admin/', include(admin.site.urls)),
]
