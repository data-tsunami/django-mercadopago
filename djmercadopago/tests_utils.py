# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.test import TestCase

from djmercadopago import services
from djmercadopago import signals


class BaseDjMercadopagoTestCase(TestCase):
    """
    Base test case for django-mercadopago.
    """

    def _disable_signals(self):
        signals.checkout_preferences_created.disconnect(sender=services.MercadoPagoService,
                                                        dispatch_uid='sample-project-checkout_preferences_created')

    def setUp(self):
        self._disable_signals()


class BaseSignalTestCase(BaseDjMercadopagoTestCase):
    """
    Base test case for signals.

    Subclasses should implement `signal_callback()`
    """

    SIGNAL = None

    def setUp(self):
        super(BaseSignalTestCase, self).setUp()
        if self.SIGNAL is None:
            raise AttributeError("Should set SIGNAL attribute")
        self.dispatch_uid = uuid.uuid4().hex
        self.checkout_preferences_created_signal = self.SIGNAL.connect(
            self.signal_callback,
            sender=services.MercadoPagoService,
            dispatch_uid=self.dispatch_uid
        )

    def tearDown(self):
        signals.checkout_preferences_created.disconnect(sender=services.MercadoPagoService,
                                                        dispatch_uid=self.dispatch_uid)

    def signal_callback(self, signal, **kwargs):
        raise NotImplemented()
