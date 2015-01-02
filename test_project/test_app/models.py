# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import uuid

# from django.db import models


def update_checkout_preference(checkout_preference, params):
    external_reference = "payment-for-user-123-{0}".format(uuid.uuid4())
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
