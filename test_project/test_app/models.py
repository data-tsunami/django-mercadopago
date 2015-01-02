# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# from django.db import models


def update_checkout_preference(checkout_preference, params):
    external_reference = "payment-for-user-123"
    checkout_preference.update({
        "items": [
            {
                "title": "My Product",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": 100,
            }
        ],
        "external_reference": external_reference,
    })
