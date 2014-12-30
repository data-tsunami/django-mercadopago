# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import importlib
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic.base import View
import mercadopago
from django.http.response import HttpResponseRedirect


logger = logging.getLogger(__name__)


class UtilsMixin(object):

    def get_as_iso8601(self, date):
        # FIXME: implement this
        return date.isoformat(b'T')[0:-7] + ".000+00:00"

    def generate_default_checkout_preference(self):
        return dict(back_urls=dict(
            success=reverse('djmercadopago:back-urls-success'),
            failure=reverse('djmercadopago:back-urls-failure'),
            pending=reverse('djmercadopago:back-urls-pending'),))

    def get_checkout_preferences(self):
        params = self.kwargs['params']

        # FIXME: report detailed report if can't get the function
        checkout_preferences = self.generate_default_checkout_preference()
        function_string = settings.DJMERCADOPAGO_CHECKOUT_PREFERENCE_BUILDER
        mod_name, func_name = function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        func(checkout_preferences, params)

        # FIXME: generate custom exception with better messages
        assert checkout_preferences.get("items")
        for item in checkout_preferences["items"]:
            assert "external_reference" in item

        return checkout_preferences

    def get_url(self, checkout_preference_result):
        if settings.DJMERCADOPAGO_SANDBOX_MODE:
            url = checkout_preference_result["response"]["sandbox_init_point"]
        else:
            url = checkout_preference_result["response"]["init_point"]

        logger.debug("Using url '%s'", url)
        return url

    def get_checkout_preference_result(self):
        mp = mercadopago.MP(settings.DJMERCADOPAGO_CLIENT_ID,
                            settings.DJMERCADOPAGO_CLIENTE_SECRET)
        logger.debug("sandbox_mode: %s",
                     settings.DJMERCADOPAGO_SANDBOX_MODE)
        mp.sandbox_mode(settings.DJMERCADOPAGO_SANDBOX_MODE)
        checkout_preferences = self.get_checkout_preferences()
        # FIXME: the next generates a request. This should be executed
        # in Celery
        checkout_preference_result = mp.create_preference(checkout_preferences)

        logger.debug("Responso of mp.create_preference(): %s",
                     checkout_preference_result)

        return checkout_preference_result


class CheckoutView(View, UtilsMixin):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        checkout_preference_result = self.get_checkout_preference_result()
        url = self.get_url(checkout_preference_result)

        logger.info("Redirecting user '%s' to '%s'",
                    request.user, url)

        return HttpResponseRedirect(url)


class CheckoutSuccessView(View):
    pass


class CheckoutFailureView(View):
    pass


class CheckoutPendingView(View):
    pass
