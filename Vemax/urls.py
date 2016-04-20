"""Vemax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from vemax.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^init$', init_view),
    url(r'^login$', login_view),
    url(r'^register$', register_view),
    url(r'^homepage$', homepage_view),

    url(r'^information$', information_view),
    url(r'^information_data$', information_data),
    url(r'^relationship$', relationship_view),
    url(r'^relationship_data$', relationship_data),

    url(r'^classify$', classify_view),
    url(r'^classify_data$', classify_data),
    url(r'^classify_detail$', classify_detail_view),

    url(r'^friend_analyse$', friend_analyse),

    url(r'^search$', search_view)
    ]
