# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid
import mock

from django.test.client import RequestFactory

from djmercadopago import signals
from djmercadopago.tests import tests_utils


# ----------------------------------------------------------------------
# SIGNAL: checkout_preferences_created
# ----------------------------------------------------------------------

class TestCheckoutPreferencesCreatedSignalHandlerIsCalled(tests_utils.BaseSignalTestCase):

    checkout_preferences_created_handler = mock.Mock()

    SIGNALS = [
        [signals.checkout_preferences_created, 'checkout_preferences_created_handler']
    ]

    def test(self):
        service = tests_utils.MercadoPagoServiceMock()
        service.do_checkout(RequestFactory().get('/'), '')

        self.assertEqual(self.checkout_preferences_created_handler.call_count, 1)


class TestCheckoutPreferencesCreatedSignalParameters(tests_utils.BaseSignalTestCase):

    SIGNALS = [
        [signals.checkout_preferences_created, 'checkout_preferences_created_handler']
    ]

    def setUp(self):
        super(TestCheckoutPreferencesCreatedSignalParameters, self).setUp()
        self.checkout_ids = []

    def checkout_preferences_created_handler(self, signal, **kwargs):
        checkout_preferences = kwargs['checkout_preferences']
        user_checkout_identifier = kwargs['user_checkout_identifier']
        request = kwargs['request']

        self.assertIsNotNone(checkout_preferences)
        self.assertIsNotNone(user_checkout_identifier)
        self.assertIsNotNone(request)

        checkout_preferences.update({
            "items": [
                {
                    "title": "some product",
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": 123.45,
                }
            ],
            "external_reference": user_checkout_identifier,
        })

        self.checkout_ids.append(user_checkout_identifier)

    def test(self):
        checkout_id = uuid.uuid4().hex
        service = tests_utils.MercadoPagoServiceMock()
        request = RequestFactory().get('/')

        service.do_checkout(request, checkout_id)
        self.assertListEqual(self.checkout_ids, [checkout_id])
