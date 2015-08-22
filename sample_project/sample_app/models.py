# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django import dispatch

from djmercadopago import models
from djmercadopago import services
from djmercadopago import signals

import uuid


PRODUCT_LIST = (
    ('product-1', {
        'NAME': 'T-Shirt',
        'PRICE': 100,
    }),
    ('product-2', {
        'NAME': 'Pants',
        'PRICE': 200,
    }),
    ('product-3', {
        'NAME': 'Shoes',
        'PRICE': 300,
    }),
)

PRODUCTS = dict(PRODUCT_LIST)


@dispatch.receiver(signals.checkout_preferences_created,
                   sender=services.MercadoPagoService,
                   dispatch_uid='sample-project-checkout_preferences_created')
def checkout_preferences_created_handler(sender, **kwargs):
    checkout_preferences = kwargs['checkout_preferences']
    user_checkout_identifier = kwargs['user_checkout_identifier']
    request = kwargs['request']

    # assert request.user.is_authenticated()
    product_info = PRODUCTS[user_checkout_identifier]

    back_urls = checkout_preferences.get('back_urls', {})
    checkout_preferences['back_urls'] = back_urls
    back_urls['success'] = request.build_absolute_uri(reverse('successful_checkout'))

    external_reference = "payment-for-user-123-{0}".format(uuid.uuid4())
    checkout_preferences.update({
        "items": [
            {
                "title": product_info['NAME'],
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": product_info['PRICE'],
            }
        ],
        "external_reference": external_reference,
    })


@dispatch.receiver(signals.pre_mp_create_preference,
                   sender=services.MercadoPagoService,
                   dispatch_uid='sample-project-pre_mp_create_preference')
def pre_mp_create_preference_handler(sender, **kwargs):
    payment = kwargs['payment']
    user_checkout_identifier = kwargs['user_checkout_identifier']
    request = kwargs['request']

    assert isinstance(payment, models.Payment)

    #
    # Here, you can save, in your models, a reference to the 'payment' instance
    # (the 'payment' instance was already saved, so it has a database 'id').
    #
    # At this point, the API call to MP was NOT done yet
    #


@dispatch.receiver(signals.post_mp_create_preference,
                   sender=services.MercadoPagoService,
                   dispatch_uid='sample-project-post_mp_create_preference')
def post_mp_create_preference_handler(sender, **kwargs):
    payment = kwargs['payment']
    user_checkout_identifier = kwargs['user_checkout_identifier']
    request = kwargs['request']

    assert isinstance(payment, models.Payment)

    #
    # At this point, the API call to MP WAS done
    #
