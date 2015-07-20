# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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


def update_checkout_preference(checkout_preference, params):
    product_info = PRODUCTS[params]

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
