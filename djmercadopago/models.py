# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core import exceptions


class DjMercadoLibreSettingsSingleton(object):
    """Encapsulates and validates the Django settings used by DjMercadoPago"""

    @staticmethod
    def _get_attr(setting_object, attribute_name):
        try:
            return setting_object[attribute_name]
        except KeyError:
            raise exceptions.ImproperlyConfigured("Value for '{0}' not found on your "
                                                  "'DJMERCADOPAGO' setting".format(attribute_name))

    def __init__(self):
        djmercadopago_settings = getattr(settings, 'DJMERCADOPAGO', None)
        if djmercadopago_settings is None:
            raise exceptions.ImproperlyConfigured("You must add 'DJMERCADOPAGO' on your Django's settings")

        self._client_id = self._get_attr(djmercadopago_settings, 'CLIENT_ID')
        self._client_secret = self._get_attr(djmercadopago_settings, 'CLIENTE_SECRET')
        self._sandbox_mode = self._get_attr(djmercadopago_settings, 'SANDBOX_MODE')
        if self._sandbox_mode not in (True, False):
            raise exceptions.ImproperlyConfigured("Value for 'DJMERCADOPAGO.SANDBOX_MODE' must be a boolean")
        self._checkout_preference_updater_function = self._get_attr(djmercadopago_settings,
                                                                    'CHECKOUT_PREFERENCE_UPDATER_FUNCTION')
        # FIXME: validate that the function referenced by '_checkout_preference_updater_function' exists

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def sandbox_mode(self):
        return self._sandbox_mode

    @property
    def checkout_preference_updater_function(self):
        return self._checkout_preference_updater_function


SETTINGS = DjMercadoLibreSettingsSingleton()


class Payment(models.Model):
    # payment_id = models.BigIntegerField(null=True)
    checkout_preferences = models.TextField()
    checkout_response = models.TextField()
    external_reference = models.TextField()
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)
