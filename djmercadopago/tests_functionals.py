# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from unittest.case import skipIf

from django.test.client import RequestFactory

from djmercadopago import services
from djmercadopago.models import Payment
from djmercadopago import signals
from djmercadopago import tests_utils


@skipIf(os.environ.get('RUN_FUNC_TEST', '').lower() == 'false',
        'Functional tests disabled')
class TestMercadoPagoService(tests_utils.BaseSignalTestCase):

    SIGNALS = [
        [signals.checkout_preferences_created, 'checkout_preferences_created_handler']
    ]

    def checkout_preferences_created_handler(self, signal, **kwargs):
        checkout_preferences = kwargs['checkout_preferences']

        external_reference = "checkout-id"
        checkout_preferences.update({
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

    def test_checkout_and_search_workflow(self):
        service = services.MercadoPagoService()
        request = RequestFactory().get('/')
        checkout_result = service.do_checkout(request, '')

        self.assertTrue(checkout_result is not None)
        self.assertTrue(isinstance(checkout_result, services.CheckoutPreferenceResult))
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
        self.assertTrue(isinstance(search_result, services.SearchResult))

    def _search_payment_by_external_reference(self):
        """Utility method to be called from CLI. Not a real test"""
        service = services.MercadoPagoService()
        search_result = service.search_payment_by_external_reference(
            os.environ['EXTERNAL_REFERENCE'])
        print "------------------------------------------------------------"
        print search_result.dump_as_string()
