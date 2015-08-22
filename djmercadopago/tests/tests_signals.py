# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid
import mock

from django.test.client import RequestFactory

from djmercadopago import models
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

    def test_checkout_preferences_created_is_called(self):
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

    def test_checkout_preferences_created_parameters(self):
        checkout_id = uuid.uuid4().hex
        service = tests_utils.MercadoPagoServiceMock()
        request = RequestFactory().get('/')

        service.do_checkout(request, checkout_id)
        self.assertListEqual(self.checkout_ids, [checkout_id])


# ----------------------------------------------------------------------
# SIGNAL: pre_mp_create_preference
# ----------------------------------------------------------------------

class TestPreMpCreatePreferenceSignalHandlerIsCalled(tests_utils.BaseSignalTestCase):

    pre_mp_create_preference_handler = mock.Mock()

    SIGNALS = [
        [signals.pre_mp_create_preference, 'pre_mp_create_preference_handler']
    ]

    def test_pre_mp_create_preference_is_called(self):
        service = tests_utils.MercadoPagoServiceMock()
        service.do_checkout(RequestFactory().get('/'), '')

        self.assertEqual(self.pre_mp_create_preference_handler.call_count, 1)


class TestPreMpCreatePreferenceSignalParameters(tests_utils.BaseSignalTestCase):

    SIGNALS = [
        [signals.pre_mp_create_preference, 'pre_mp_create_preference_handler']
    ]

    def pre_mp_create_preference_handler(self, signal, **kwargs):
        payment = kwargs['payment']
        user_checkout_identifier = kwargs['user_checkout_identifier']
        request = kwargs['request']

        self.assertIsNotNone(payment)
        self.assertIsNotNone(user_checkout_identifier)
        self.assertIsNotNone(request)

        self.assertTrue(isinstance(payment, models.Payment))
        self.assertTrue(payment.id > 0)
        self.assertTrue(payment.checkout_preferences)
        self.assertFalse(payment.checkout_response)

    def test_pre_mp_create_preference_parameters(self):
        service = tests_utils.MercadoPagoServiceMock()
        service.do_checkout(RequestFactory().get('/'), '')


# ----------------------------------------------------------------------
# SIGNAL: post_mp_create_preference
# ----------------------------------------------------------------------

class TestPostMpCreatePreferenceSignalHandlerIsCalled(tests_utils.BaseSignalTestCase):

    post_mp_create_preference_handler = mock.Mock()

    SIGNALS = [
        [signals.post_mp_create_preference, 'post_mp_create_preference_handler']
    ]

    def test_post_mp_create_preference_is_called(self):
        service = tests_utils.MercadoPagoServiceMock()
        service.do_checkout(RequestFactory().get('/'), '')

        self.assertEqual(self.post_mp_create_preference_handler.call_count, 1)


class TestPostMpCreatePreferenceSignalParameters(tests_utils.BaseSignalTestCase):

    SIGNALS = [
        [signals.post_mp_create_preference, 'post_mp_create_preference_handler']
    ]

    def post_mp_create_preference_handler(self, signal, **kwargs):
        payment = kwargs['payment']
        user_checkout_identifier = kwargs['user_checkout_identifier']
        request = kwargs['request']

        self.assertIsNotNone(payment)
        self.assertIsNotNone(user_checkout_identifier)
        self.assertIsNotNone(request)

        self.assertTrue(isinstance(payment, models.Payment))
        self.assertTrue(payment.id > 0)
        self.assertTrue(payment.checkout_preferences)
        self.assertTrue(payment.checkout_response)

    def test_post_mp_create_preference_parameters(self):
        service = tests_utils.MercadoPagoServiceMock()
        service.do_checkout(RequestFactory().get('/'), '')
