# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

import uuid

from django.core.urlresolvers import reverse


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


def update_checkout_preference(checkout_preference, param, request):
    """
    This function is configured in the settings file, in the
    variable 'DJMERCADOPAGO', with key 'CHECKOUT_PREFERENCE_UPDATER_FUNCTION'.

        DJMERCADOPAGO = {

            (...)

            'CHECKOUT_PREFERENCE_UPDATER_FUNCTION':
                'sample_app.models.update_checkout_preference',
        }

    Parameters
    ----------

    * `param`: the same string used when created the link to the `djmercadopago:checkout` view.
               Example: if the URL was generated with:

                   {% url 'djmercadopago:checkout' product_id %}

               the value of `param` would be `product_id`

               You can use the `product_id` to lookup the the product's information
               in the database.
    """

    # assert request.user.is_authenticated()

    # 'params' is the argument {% url 'djmercadopago:checkout' product.0 %}
    product_info = PRODUCTS[param]

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
