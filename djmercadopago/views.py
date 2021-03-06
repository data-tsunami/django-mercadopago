# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View

from djmercadopago.services import MercadoPagoService


logger = logging.getLogger(__name__)


class CheckoutView(View):

    http_method_names = ['get']

    def __init__(self, **kwargs):
        super(CheckoutView, self).__init__(**kwargs)
        self.service = MercadoPagoService()

    def get(self, request, *args, **kwargs):
        user_checkout_identifier = self.kwargs['user_checkout_identifier']

        result = self.service.do_checkout(request,
                                          user_checkout_identifier)
        url = result.url
        logger.info("Redirecting user '%s' to '%s'", request.user, url)

        return HttpResponseRedirect(url)


class CheckoutSuccessView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("success")


class CheckoutFailureView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("failure")


class CheckoutPendingView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("pending")
