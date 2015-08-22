# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import pprint
from copy import deepcopy

import mercadopago

from djmercadopago import models
from djmercadopago import signals


logger = logging.getLogger(__name__)


class CheckoutPreference(object):
    """Encapsulate the checkout preference (dict), plus
    utility methods.
    """
    def __init__(self, checkout_preferences):
        self._preferences = checkout_preferences

        # FIXME: generate custom exception with better messages
        if "items" not in self._preferences:
            logger.warn("The 'checkout preferences' received does NOT have 'items'")

    # FIXME: inherit from dict?

    @property
    def preferences(self):
        return deepcopy(self._preferences)

    @property
    def external_reference(self):
        return self._preferences.get("external_reference", None)

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

    def __init__(self):
        self.mp = mercadopago.MP(models.SETTINGS.client_id, models.SETTINGS.client_secret)
        logger.debug("Returning MP instance with sandbox_mode: %s", models.SETTINGS.sandbox_mode)
        self.mp.sandbox_mode(models.SETTINGS.sandbox_mode)

    def get_as_iso8601(self, date):
        # FIXME: implement this
        return date.isoformat(b'T')[0:-7] + ".000+00:00"

    def do_checkout(self, request, user_checkout_identifier):
        """Do the checkout process.

        :returns: CheckoutPreferenceResult
        """
        checkout_preferences_dict = {}
        signals.checkout_preferences_created.send(
            sender=MercadoPagoService,
            checkout_preferences=checkout_preferences_dict,
            user_checkout_identifier=user_checkout_identifier,
            request=request
        )

        checkout_preferences = CheckoutPreference(checkout_preferences_dict)

        logger.debug("do_checkout(): checkout_preferences:\n%s", checkout_preferences.dump_as_string())

        payment = models.Payment()
        payment.checkout_preferences = checkout_preferences.dump_as_string()
        payment.external_reference = checkout_preferences.external_reference
        payment.save()

        signals.pre_mp_create_preference.send(
            sender=MercadoPagoService,
            payment=payment,
            user_checkout_identifier=user_checkout_identifier,
            request=request
        )

        # FIXME: the next line generates a http request. This should be executed asynchronously (ej: Celery)
        # FIXME: in case of error, it shoud be saved in 'checkout_response'?
        checkout_preference_result_dict = self.mp.create_preference(checkout_preferences.preferences)

        checkout_preference_result = CheckoutPreferenceResult(
            checkout_preference_result_dict, payment)

        logger.debug("do_checkout(): checkout_preference_result:\n%s", checkout_preference_result.dump_as_string())

        payment.checkout_response = checkout_preference_result.dump_as_string()
        payment.save()

        signals.post_mp_create_preference.send(
            sender=MercadoPagoService,
            payment=payment,
            create_preference_result=checkout_preference_result_dict,
            user_checkout_identifier=user_checkout_identifier,
            request=request
        )

        return checkout_preference_result

    def search_payment_by_external_reference(self, external_reference):
        """Search payments by 'external reference'

        :returns: SearchResult
        """
        filters = {
            "site_id": "MLA",  # Argentina: MLA; Brasil: MLB
            "external_reference": external_reference,
        }
        # FIXME: move 'site_id' to settings

        logger.debug("search_payment_by_external_reference(): "
                     "filters:\n%s",
                     filters)

        search_result_dict = self.mp.search_payment(filters)
        search_result = SearchResult(search_result_dict)

        logger.debug("search_payment_by_external_reference(): search_result:\n%s", search_result.dump_as_string())

        return search_result
