# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import importlib
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
import mercadopago
import pprint


logger = logging.getLogger(__name__)


class BackUrlsBuilder(object):
    """Generates the URLs for the 'back-urls'
    checkout preference
    """

    def __init__(self):
        self._success_url = None
        self._failure_url = None
        self._pending_url = None

    def build(self,
              request,
              success_url=None,
              failure_url=None,
              pending_url=None):
        """Generate default urls"""
        self._success_url = success_url or request.build_absolute_uri(
            reverse('djmercadopago:back-urls-success'))
        self._failure_url = failure_url or request.build_absolute_uri(
            reverse('djmercadopago:back-urls-failure'))
        self._pending_url = pending_url or request.build_absolute_uri(
            reverse('djmercadopago:back-urls-pending'))
        return self

    @property
    def success_url(self):
        return self._success_url

    @property
    def failure_url(self):
        return self._failure_url

    @property
    def pending_url(self):
        return self._pending_url


class CheckoutPreference(object):
    """Encapsulate the checkout preference (dict), plus
    utility methods.
    """
    def __init__(self, checkout_preferences):
        self._preferences = checkout_preferences

        # FIXME: generate custom exception with better messages
        # FIXME: add doc about requeriment of 'external_reference'
        assert self._preferences.get("items")
        for item in self._preferences["items"]:
            assert "external_reference" in item

    @property
    def preferences(self):
        return self._preferences

    def dump_as_string(self):
        return pprint.pformat(self._preferences)


class CheckoutPreferenceResult(object):
    """Encapsulate the RESULT of checkout (dict), plus
    utility methods
    """
    def __init__(self, result):
        self._result = result

    @property
    def url(self):
        assert "response" in self._result
        if settings.DJMERCADOPAGO_SANDBOX_MODE:
            url = self._result["response"]["sandbox_init_point"]
        else:
            url = self._result["response"]["init_point"]

        logger.debug("url: '%s' (sandbox mode: %s)", url,
                     settings.DJMERCADOPAGO_SANDBOX_MODE)
        return url

    def dump_as_string(self):
        return pprint.pformat(self._result)


class MercadoPagoService(object):

    def get_as_iso8601(self, date):
        # FIXME: implement this
        return date.isoformat(b'T')[0:-7] + ".000+00:00"

    def _default_checkout_preference_dict(self, back_urls_builder):
        """Generates a checkout preference with default settings"""
        assert isinstance(back_urls_builder, BackUrlsBuilder)
        return dict(back_urls=dict(
            success=back_urls_builder.success_url,
            failure=back_urls_builder.failure_url,
            pending=back_urls_builder.pending_url))

    def _get_update_preferences_function(self):
        """Returns the functions (implemented by the user) updates
        the checkout preferences dict.
        """
        function_string = settings.\
            DJMERCADOPAGO_CHECKOUT_PREFERENCE_UPDATER_FUNCTION
        mod_name, func_name = function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        assert callable(func)
        return func

    def _generate_checkout_preferences(self, user_params, back_urls_builder):
        """Returns CheckoutPreference"""
        update_preferences_function = \
            self._get_update_preferences_function()

        # FIXME: report detailed error if can't get the function
        checkout_preferences = self._default_checkout_preference_dict(
            back_urls_builder)
        update_preferences_function(checkout_preferences, user_params)

        return CheckoutPreference(checkout_preferences)

    def _call_mp(self, mp, checkout_preferences):
        assert isinstance(checkout_preferences, CheckoutPreference)
        checkout_preference_result = mp.create_preference(
            checkout_preferences.preferences)
        return checkout_preference_result

    def get_mercadopago(self):
        """Returns MP instance"""
        mp = mercadopago.MP(settings.DJMERCADOPAGO_CLIENT_ID,
                            settings.DJMERCADOPAGO_CLIENTE_SECRET)
        logger.debug("Returning MP instance with sandbox_mode: %s",
                     settings.DJMERCADOPAGO_SANDBOX_MODE)
        mp.sandbox_mode(settings.DJMERCADOPAGO_SANDBOX_MODE)
        return mp

    def do_checkout(self, user_params, back_urls_builder):
        """Do the checkout process.

        :returns: CheckoutPreferenceResult
        """
        mp = self.get_mercadopago()
        checkout_preferences = self._generate_checkout_preferences(
            user_params, back_urls_builder)

        logger.debug("do_checkout(): checkout_preferences:\n%s",
                     checkout_preferences.dump_as_string())

        # FIXME: the next generates a http request. This should be executed
        # in Celery
        checkout_preference_result_dict = self._call_mp(mp,
                                                        checkout_preferences)
        checkout_preference_result = CheckoutPreferenceResult(
            checkout_preference_result_dict)

        logger.debug("do_checkout(): checkout_preference_result:\n%s",
                     checkout_preference_result.dump_as_string())

        return
