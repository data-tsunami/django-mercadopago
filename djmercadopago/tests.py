# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings


from djmercadopago.services import (
    MercadoPagoService, BackUrlsBuilder, CheckoutPreferenceResult, SearchResult)
from djmercadopago.models import Payment


DJMERCADOPAGO_UNITTEST_SETTINGS = {
    'CLIENT_ID': settings.DJMERCADOPAGO['CLIENT_ID'],
    'CLIENTE_SECRET': settings.DJMERCADOPAGO['CLIENTE_SECRET'],
    'SANDBOX_MODE': True,  # Always True for unittests
    'CHECKOUT_PREFERENCE_UPDATER_FUNCTION':
        'djmercadopago.tests.update_checkout_preference',
}


def update_checkout_preference(checkout_preference, checkout_identifier, request):
    external_reference = "checkout-id"
    checkout_preference.update({
        "items": [
            {
                "title": "some product",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": 123.45,
            }
        ],
        "external_reference": external_reference,
    })


class BackUrlsBuilderMock(BackUrlsBuilder):

    def __init__(self):
        self._success_url = 'https://www.google.com/'
        self._failure_url = 'https://www.google.com/'
        self._pending_url = 'https://www.google.com/'


class TestMercadoPagoService(TestCase):

    @override_settings(DJMERCADOPAGO=DJMERCADOPAGO_UNITTEST_SETTINGS)
    def test_checkout_and_search(self):
        service = MercadoPagoService()

        from django.test.client import RequestFactory

        request = RequestFactory().get('/')
        checkout_result = service.do_checkout(request, '', BackUrlsBuilderMock())

        self.assertTrue(checkout_result is not None)
        self.assertTrue(isinstance(checkout_result, CheckoutPreferenceResult))
        self.assertTrue(checkout_result.url)
        self.assertTrue(checkout_result.external_reference)
        self.assertTrue(checkout_result.payment)
        self.assertTrue(checkout_result.payment.id is not None)

        payment = Payment.objects.get(id=checkout_result.payment.id)
        self.assertTrue(payment.checkout_preferences)
        self.assertTrue(payment.checkout_response)
        self.assertTrue(payment.checkout_response)

        search_result = service.search_payment_by_external_reference(
            checkout_result.external_reference)

        self.assertTrue(search_result is not None)
        self.assertTrue(isinstance(search_result, SearchResult))

    def _search_payment_by_external_reference(self):
        """Utility method to be called from CLI. Not a real test"""
        service = MercadoPagoService()
        search_result = service.search_payment_by_external_reference(
            os.environ['EXTERNAL_REFERENCE'])
        print "------------------------------------------------------------"
        print search_result.dump_as_string()
