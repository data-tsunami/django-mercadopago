# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from djmercadopago.services import MercadoPagoService, BackUrlsBuilder, \
    CheckoutPreferenceResult
import os


class BackUrlsBuilderMock(BackUrlsBuilder):

    def __init__(self):
        self._success_url = 'https://www.google.com/'
        self._failure_url = 'https://www.google.com/'
        self._pending_url = 'https://www.google.com/'


class TestMercadoPagoService(TestCase):

    def test_checkout_and_search(self):
        service = MercadoPagoService()

        checkout_result = service.do_checkout('', BackUrlsBuilderMock())
        assert isinstance(checkout_result, CheckoutPreferenceResult)
        self.assertTrue(checkout_result.url)
        self.assertTrue(checkout_result.external_reference)

        search_result = service.search_payment_by_external_reference(
            checkout_result.external_reference)

    def _search_payment_by_external_reference(self):
        """Utility method to be called from CLI. Not a real test"""
        service = MercadoPagoService()
        search_result = service.search_payment_by_external_reference(
            os.environ['EXTERNAL_REFERENCE'])
        print "------------------------------------------------------------"
        print search_result.dump_as_string()
