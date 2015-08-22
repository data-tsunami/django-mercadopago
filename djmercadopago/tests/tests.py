# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test.client import RequestFactory

from djmercadopago import signals
from djmercadopago.tests import tests_utils


class TestExternalReferenceIsNotRequired(tests_utils.BaseSignalTestCase):

    SIGNALS = [
        [signals.checkout_preferences_created, 'checkout_preferences_created_handler']
    ]

    def checkout_preferences_created_handler(self, signal, **kwargs):
        checkout_preferences = kwargs['checkout_preferences']
        checkout_preferences.update({
            "items": [
                {
                    "title": "some product",
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": 123.45,
                }
            ],
        })

    def test(self):
        service = tests_utils.MercadoPagoServiceMock()
        request = RequestFactory().get('/')
        checkout_preference_result = service.do_checkout(request, '')

        self.assertEqual(checkout_preference_result.external_reference, '')
