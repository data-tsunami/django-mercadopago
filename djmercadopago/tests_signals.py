# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.test.client import RequestFactory

from djmercadopago import services
from djmercadopago import signals
from djmercadopago import tests_utils


class UpdaterFunctionCalledException(Exception):
    pass


class TestCheckoutPreferencesCreatedSignalHandlerIsCalled(tests_utils.BaseSignalTestCase):

    SIGNAL = signals.checkout_preferences_created

    def signal_callback(self, signal, **kwargs):
        raise UpdaterFunctionCalledException()

    def test(self):
        service = services.MercadoPagoService()
        request = RequestFactory().get('/')

        with self.assertRaises(UpdaterFunctionCalledException):
            service.do_checkout(request, '')


class TestCheckoutPreferencesCreatedSignalParameters(tests_utils.BaseSignalTestCase):

    SIGNAL = signals.checkout_preferences_created

    def setUp(self):
        super(TestCheckoutPreferencesCreatedSignalParameters, self).setUp()
        self.checkout_ids = []

    def signal_callback(self, signal, **kwargs):
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
        service = services.MercadoPagoService()
        request = RequestFactory().get('/')

        service.do_checkout(request, checkout_id)
        self.assertListEqual(self.checkout_ids, [checkout_id])