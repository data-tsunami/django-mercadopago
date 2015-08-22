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
        """Disconnect the signals used in the sample application"""
        signals.checkout_preferences_created.disconnect(sender=services.MercadoPagoService,
                                                        dispatch_uid='sample-project-checkout_preferences_created')

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
