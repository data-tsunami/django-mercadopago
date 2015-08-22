# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.test import TestCase

from djmercadopago import services
from djmercadopago import signals


class MercadoPagoServiceMock(services.MercadoPagoService):

    def __init__(self, *args, **kwargs):
        super(MercadoPagoServiceMock, self).__init__(*args, **kwargs)
        self._created_preferences = []

        # FIXME: use mock library
        self.mp.create_preference = self._create_preference
        self.mp.search_payment = self._search_payment

    def _create_preference(self, preference):
        # FIXME: create better response (use 'external_reference', 'back_urls', better dates, etc)
        identifier = uuid.uuid4().hex
        external_reference = preference.get('external_reference', '')
        response = {
            'response': {
                u'additional_info': u'',
                u'auto_return': u'',
                u'back_urls': {u'failure': u'',
                               u'pending': u'',
                               u'success': u''},
                u'client_id': u'963',
                u'collector_id': 173936381,
                u'date_created': u'2015-08-22T11:44:43.015-04:00',
                u'expiration_date_from': None,
                u'expiration_date_to': None,
                u'expires': False,
                u'external_reference': external_reference,
                u'id': identifier,
                u'init_point': u'https://www.mercadopago.com/mla/checkout/start?pref_id=' + identifier,
                u'items': [{u'category_id': u'',
                            u'currency_id': u'ARS',
                            u'description': u'',
                            u'id': u'',
                            u'picture_url': u'',
                            u'quantity': 1,
                            u'title': u'some product',
                            u'unit_price': 123.45}],
                u'marketplace': u'NONE',
                u'marketplace_fee': 0,
                u'notification_url': None,
                u'operation_type': u'regular_payment',
                u'payer': {u'address': {u'street_name': u'',
                                        u'street_number': None,
                                        u'zip_code': u''},
                           u'date_created': u'',
                           u'email': u'',
                           u'identification': {u'number': u'', u'type': u''},
                           u'name': u'',
                           u'phone': {u'area_code': u'', u'number': u''},
                           u'surname': u''},
                u'payment_methods': {u'default_installments': None,
                                     u'default_payment_method_id': None,
                                     u'excluded_payment_methods': [{u'id': u''}],
                                     u'excluded_payment_types': [{u'id': u''}],
                                     u'installments': None},
                u'sandbox_init_point': u'https://sandbox.mercadopago.com/mla/checkout/pay?pref_id=' + identifier,
                u'shipments': {u'receiver_address': {u'apartment': u'',
                                                     u'floor': u'',
                                                     u'street_name': u'',
                                                     u'street_number': None,
                                                     u'zip_code': u''}}},
            'status': 201
        }
        self._created_preferences.append([preference, response])
        return response

    def _search_payment(self, *args, **kwargs):
        raise NotImplemented()


class BaseDjMercadopagoTestCase(TestCase):
    """
    Base test case for django-mercadopago.
    """

    SAMPLE_APP_DISPATCH_UIDS = [
        'sample-project-checkout_preferences_created',
        'sample-project-pre_mp_create_preference',
        'sample-project-post_mp_create_preference',
    ]

    def _disable_signals(self):
        """Disconnect the signals used in the sample application"""
        for dispatch_uid in self.SAMPLE_APP_DISPATCH_UIDS:
            signals.checkout_preferences_created.disconnect(
                sender=services.MercadoPagoService,
                dispatch_uid=dispatch_uid)

    def setUp(self):
        self._disable_signals()


class BaseSignalTestCase(BaseDjMercadopagoTestCase):
    """
    Base test case for signals.

    Subclasses should implement `signal_callback()`
    """

    SIGNALS = None

    def setUp(self):
        super(BaseSignalTestCase, self).setUp()
        if self.SIGNALS is None:
            raise AttributeError("Should set SIGNALS attribute")

        self.dispatch_uids = []

        for signal, handler_name in self.SIGNALS:
            handler = getattr(self, handler_name)
            dispatch_uid = uuid.uuid4().hex
            signal.connect(
                handler,
                sender=services.MercadoPagoService,
                dispatch_uid=dispatch_uid
            )
            self.dispatch_uids.append(dispatch_uid)

    def tearDown(self):
        for dispatch_uid in self.dispatch_uids:
            signals.checkout_preferences_created.disconnect(sender=services.MercadoPagoService,
                                                            dispatch_uid=dispatch_uid)

    def signal_callback(self, signal, **kwargs):
        raise NotImplemented()
