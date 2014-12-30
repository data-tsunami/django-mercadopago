# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import importlib
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
import mercadopago


logger = logging.getLogger(__name__)


class CheckoutPreference(object):
    """Encapsulate the checkout preference (dict), plus
    utility methods
    """
    def __init__(self, checkout_preferences):
        self._preferences = checkout_preferences

        # FIXME: generate custom exception with better messages
        # FIXME: add doc about requeriment of 'external_reference'
        assert self._preferences.get("items")
        for item in self._preferences["items"]:
            assert "external_reference" in item


class CheckoutPreferenceResult(object):
    """Encapsulate the RESULT of checkout (dict), plus
    utility methods
    """
    def __init__(self, result):
        self._result = result

    def get_url(self):
        assert "response" in self._result
        if settings.DJMERCADOPAGO_SANDBOX_MODE:
            url = self._result["response"]["sandbox_init_point"]
        else:
            url = self._result["response"]["init_point"]

        logger.debug("get_url(): '%s' (sandbox mode: %s)",
                     url,
                     settings.DJMERCADOPAGO_SANDBOX_MODE)
        return url


class MercadoPagoService(object):

    def get_as_iso8601(self, date):
        # FIXME: implement this
        return date.isoformat(b'T')[0:-7] + ".000+00:00"

    def generate_default_checkout_preference_dict(self):
        return dict(back_urls=dict(
            success=reverse('djmercadopago:back-urls-success'),
            failure=reverse('djmercadopago:back-urls-failure'),
            pending=reverse('djmercadopago:back-urls-pending'),))

    def get_update_preferences_callback(self):
        function_string = settings.DJMERCADOPAGO_CHECKOUT_PREFERENCE_BUILDER
        mod_name, func_name = function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        return func

    def get_checkout_preferences(self, user_params):
        """Returns CheckoutPreference"""
        update_preferences_callback = \
            self.generate_default_checkout_preference_dict()

        # FIXME: report detailed report if can't get the function
        checkout_preferences = self.generate_default_checkout_preference()
        update_preferences_callback(checkout_preferences, user_params)

        return CheckoutPreference(checkout_preferences)

    def do_checkout(self, user_params):
        mp = mercadopago.MP(settings.DJMERCADOPAGO_CLIENT_ID,
                            settings.DJMERCADOPAGO_CLIENTE_SECRET)
        logger.debug("sandbox_mode: %s",
                     settings.DJMERCADOPAGO_SANDBOX_MODE)
        mp.sandbox_mode(settings.DJMERCADOPAGO_SANDBOX_MODE)
        checkout_preferences = self.get_checkout_preferences(user_params)
        # FIXME: the next generates a http request. This should be executed
        # in Celery
        checkout_preference_result = mp.create_preference(checkout_preferences)

        logger.debug("Responso of mp.create_preference(): %s",
                     checkout_preference_result)

        return CheckoutPreferenceResult(checkout_preference_result)
