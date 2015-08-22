# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import dispatch


checkout_preferences_created = dispatch.Signal(providing_args=["checkout_preferences",
                                                               "user_checkout_identifier",
                                                               "request"])
"""
This signal is dispatched after the `checkout_preferences` dict is created, to
allow the user of django-mercadopago to update the `checkout_preferences` instance:

* add items and prices
* add urls
* validate user permissions
* etc.

To receive this signal, you can use:

    @receiver(checkout_preferences_created, sender=MercadoPagoService)
    def my_callback(sender, **kwargs)
        checkout_preferences = kwargs['checkout_preferences']
        user_checkout_identifier = kwargs['user_checkout_identifier']
        request = kwargs['request']

        (...)
"""
