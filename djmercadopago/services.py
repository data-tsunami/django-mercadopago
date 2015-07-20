# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from copy import deepcopy
import importlib
import logging
import pprint

import mercadopago
from django.core.urlresolvers import reverse

from djmercadopago import models


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
        assert "external_reference" in self._preferences

    @property
    def preferences(self):
        return deepcopy(self._preferences)

    @property
    def external_reference(self):
        return self._preferences["external_reference"]

    def dump_as_string(self):
        return pprint.pformat(self._preferences)


class CheckoutPreferenceResult(object):
    """Encapsulate the RESULT of checkout (dict), the Payment instance,
    plus utility methods
    """
    def __init__(self, result, payment):
        self._result = result
        self._payment = payment

    @property
    def result(self):
        return deepcopy(self._result)

    @property
    def payment(self):
        return self._payment

    @property
    def external_reference(self):
        return self._result["response"]["external_reference"]

    @property
    def url(self):
        assert "response" in self._result
        if models.SETTINGS.sandbox_mode:
            url = self._result["response"]["sandbox_init_point"]
        else:
            url = self._result["response"]["init_point"]

        logger.debug("url: '%s' (sandbox mode: %s)", url, models.SETTINGS.sandbox_mode)
        return url

    def dump_as_string(self):
        return pprint.pformat(self._result)


class SearchResult(object):
    """Encapsulate the result of a search, plus
    utility methods.
    """
    def __init__(self, search_result):
        self._search_result = search_result

        # FIXME: generate custom exception with better messages
        assert "response" in self._search_result
        assert "results" in self._search_result["response"]

    def get_payments(self):
        return deepcopy(self._search_result["response"]["results"])

    def dump_as_string(self):
        return pprint.pformat(self._search_result)


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
        function_string = models.SETTINGS.checkout_preference_updater_function
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

    def _call_mp_create_preference(self, mp, checkout_preferences):
        assert isinstance(checkout_preferences, CheckoutPreference)
        checkout_preference_result = mp.create_preference(
            checkout_preferences.preferences)
        return checkout_preference_result

    def get_mercadopago(self):
        """Returns MP instance"""
        mp = mercadopago.MP(models.SETTINGS.client_id,
                            models.SETTINGS.client_secret)
        logger.debug("Returning MP instance with sandbox_mode: %s",
                     models.SETTINGS.sandbox_mode)
        mp.sandbox_mode(models.SETTINGS.sandbox_mode)
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

        payment = models.Payment()
        payment.checkout_preferences = checkout_preferences.dump_as_string()
        payment.external_reference = checkout_preferences.external_reference
        payment.save()

        # FIXME: the next generates a http request. This should be executed
        # in Celery
        checkout_preference_result_dict = self._call_mp_create_preference(
            mp, checkout_preferences)
        checkout_preference_result = CheckoutPreferenceResult(
            checkout_preference_result_dict, payment)

        logger.debug("do_checkout(): checkout_preference_result:\n%s",
                     checkout_preference_result.dump_as_string())

        payment.checkout_response = checkout_preference_result.dump_as_string()
        payment.save()

        return checkout_preference_result

    def search_payment_by_external_reference(self, external_reference):
        """Search payments by 'external reference'

        :returns: SearchResult
        """
        mp = self.get_mercadopago()

        filters = {
            "site_id": "MLA",  # Argentina: MLA; Brasil: MLB
            "external_reference": external_reference,
        }
        # FIXME: move 'site_id' to settings

        logger.debug("search_payment_by_external_reference(): "
                     "filters:\n%s",
                     filters)

        search_result_dict = mp.search_payment(filters)
        search_result = SearchResult(search_result_dict)

        logger.debug("search_payment_by_external_reference(): "
                     "search_result:\n%s",
                     search_result.dump_as_string())

        return search_result
