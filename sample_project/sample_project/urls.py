# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin
from sample_app.views import HomeView, SuccessfulCheckoutView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^success/$', SuccessfulCheckoutView.as_view(), name='successful_checkout'),

    url(r'^mp/', include('djmercadopago.urls', namespace="djmercadopago")),
    url(r'^admin/', include(admin.site.urls)),
)
