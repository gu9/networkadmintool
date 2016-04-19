"""FinalProject URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^router/form/$','router.views.RouterRegisteration'),
    url(r'^router/index/$','router.views.allhostrequest'),
    url(r'^router/interface/$','router.views.show_interface_view'),
    url(r'^router/parameter/$','router.views.performance_view'),
    url(r'^router/vrfshow/$','router.views.vrf_show'),
    url(r'^router/vrfdropdown/$','router.views.allvrfrequest'),
    url(r'^router/logoutview/$','router.views.logout_view'),
    url(r'^router/iplookup/$','router.views.ip_lookup_view'),
    url(r'^router/protocol/$','router.views.protocol_view'),
    
   
    
   
]
