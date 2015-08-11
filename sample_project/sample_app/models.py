# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

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


def update_checkout_preference(checkout_preference, checkout_identifier, request):
    # assert request.user.is_authenticated()

    product_info = PRODUCTS[checkout_identifier]

    checkout_preference['back_urls']['success'] = request.build_absolute_uri(reverse('successful_checkout'))

    external_reference = "payment-for-user-123-{0}".format(uuid.uuid4())
    checkout_preference.update({
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
