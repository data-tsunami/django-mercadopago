# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url
from djmercadopago.views import (CheckoutView,
                                 CheckoutSuccessView,
                                 CheckoutFailureView,
                                 CheckoutPendingView)


urlpatterns = patterns(
    '',
    url(r'^checkout/(?P<params>.+)/$',
        CheckoutView.as_view(),
        name='checkout'),

    url(r'^back-urls/success/$',
        CheckoutSuccessView.as_view(),
        name='back-urls-success'),

    url(r'^back-urls/failure/$',
        CheckoutFailureView.as_view(),
        name='back-urls-failure'),

    url(r'^back-urls/pending/$',
        CheckoutPendingView.as_view(),
        name='back-urls-pending'),

)
