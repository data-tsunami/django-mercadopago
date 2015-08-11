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

    * `checkout_preference`: dictionary with the checkout preferences to call the MP api.
                             You need to populate this object with the required information,
                             including items, back urls, etc.

    * `param`: the same string used when created the link to the `djmercadopago:checkout` view.
               Example: if the URL was generated with:

                   {% url 'djmercadopago:checkout' purchase_order.id %}

               the value of `param` would be `purchase_order.id`

               You can use the `purchase_order.id` to lookup the the products
               included in the `purchase_order`

    * `request`: this allows you:
                 (a) to create absolute URLs
                 (b) get any data from session (in case you use a session-based shopping cart)
                 (c) get the User (for example, to validate that the current user is
                     the owner of the `purchase_order`)
    """

    # assert request.user.is_authenticated()

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
