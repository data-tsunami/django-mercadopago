# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core import exceptions


class DjMercadoLibreSettings(object):
    """Encapsulates and validates the Django settings used by DjMercadoPago"""

    @staticmethod
    def _get_djmp():
        djmercadopago_settings = getattr(settings, 'DJMERCADOPAGO', None)
        if djmercadopago_settings is None:
            raise exceptions.ImproperlyConfigured("You must add 'DJMERCADOPAGO' on your Django's settings")
        return djmercadopago_settings

    def _get_attr(self, attribute_name):
        try:
            return self._get_djmp()[attribute_name]
        except KeyError:
            raise exceptions.ImproperlyConfigured("Value for '{0}' not found on your "
                                                  "'DJMERCADOPAGO' setting".format(attribute_name))

    @property
    def client_id(self):
        return self._get_attr('CLIENT_ID')

    @property
    def client_secret(self):
        return self._get_attr('CLIENT_SECRET')

    @property
    def sandbox_mode(self):
        sandbox_mode = self._get_attr('SANDBOX_MODE')
        if sandbox_mode not in (True, False):
            raise exceptions.ImproperlyConfigured("Value for 'DJMERCADOPAGO.SANDBOX_MODE' must be a boolean")
        return sandbox_mode

    @property
    def checkout_preference_updater_function(self):
        # FIXME: validate that the function referenced by '_checkout_preference_updater_function' exists
        return self._get_attr('CHECKOUT_PREFERENCE_UPDATER_FUNCTION')


SETTINGS = DjMercadoLibreSettings()


class Payment(models.Model):
    # payment_id = models.BigIntegerField(null=True)
    checkout_preferences = models.TextField()
    checkout_response = models.TextField()
    external_reference = models.TextField()
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)
