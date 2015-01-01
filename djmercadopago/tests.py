# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from djmercadopago.services import MercadoPagoService, BackUrlsBuilder,\
    CheckoutPreferenceResult


class BackUrlsBuilderMock(BackUrlsBuilder):
    def __init__(self):
        self._success_url = 'https://www.google.com/'
        self._failure_url = 'https://www.google.com/'
        self._pending_url = 'https://www.google.com/'


class TestMercadoPagoService(TestCase):

    def test(self):
        service = MercadoPagoService()
        checkout_result = service.do_checkout('', BackUrlsBuilderMock())
        assert isinstance(checkout_result, CheckoutPreferenceResult)
        checkout_result.url
