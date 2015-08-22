=============
djmercadopago
=============

djmercadopago is a simple Django app to use MercadoPago


THIS IS WIP. THIS DOESN'T WORK YET.

PLEASE, THINK TWICE BEFORE USING THIS ON A PRODUCTION ENVIRONMENT.


Quick start
-----------

1. Add "djmercadopago" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'djmercadopago',
    )

2. Include the djmercadopago URLconf in your project urls.py like this::

    url(r'^mp/', include('djmercadopago.urls', namespace="djmercadopago")),

3. Implement the function that populates the **checkout preferences** dict, and attach it to the signal::

    from django import dispatch
    from djmercadopago import services
    from djmercadopago import signals

    @dispatch.receiver(signals.checkout_preferences_created,
                       sender=services.MercadoPagoService,
                       dispatch_uid='some-id-for-this-signal-handler')
    def my_checkout_preferences_updater(sender, **kwargs):
        checkout_preferences = kwargs['checkout_preferences']
        user_checkout_identifier = kwargs['user_checkout_identifier']
        request = kwargs['request']

        # Here you can add items, set back-urls, etc.

4. Configure your settings::

    DJMERCADOPAGO = {
        'CLIENT_ID': 'YOUR-MERCADOPAGO-CLIENT-ID',
        'CLIENT_SECRET': 'YOUR-MERCADOPAGO-SECRET',
        'SANDBOX_MODE': True,
    }

5. Run **python manage.py migrate** to create the djmercadopago models.

6. In your template, add a link to the checkout view::

    <a href="{% url 'djmercadopago:checkout' 'CHECKOUT_ID' %}">Checkout</a>


The ``CHECKOUT_ID`` is some identifier of the shopping cart, or purchase order, or whatever you
use to hold the items the user wants to pay. This identifier is passed to the function that populates
the ``checkout preferences`` dict, so you can query the database using that identifier.

If you have the shopping cart contents in session, you won't need an identifier.

Function that populates the `checkout preferences` dict
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

When the ``checkout_preferences_created`` signal is sent, 3 parameters are provided:

    * checkout_preferences
    * user_checkout_identifier
    * request

Parameter: checkout_preference
******************************

Dictionary with the checkout preferences to call the MP api.
You need to populate this object with the required information,
including items, back urls, etc.

Parameter: user_checkout_identifier
***********************************

The same string used when created the link to the ``djmercadopago:checkout`` view.

Example: if the URL was generated with::

   {% url 'djmercadopago:checkout' purchase_order.id %}

the value of ``user_checkout_identifier`` would be the value of ``purchase_order.id``

Parameter: request
******************

This allows you:

* to create absolute URLs
* get any data from session (in case you use a session-based shopping cart)
* get the User (for example, to validate that the current user is the owner of the ``purchase_order``)


Payment model
-------------

Before calling MP API, an instance of ``Payment`` is created. The same instances is
updated with the response.

If you need to persist a reference to the ``Payment`` instance, you can register
to the post_save signal of the model (see:
https://docs.djangoproject.com/en/1.7/ref/signals/#django.db.models.signals.post_save ).

The signal will be generated twice, since save() is called two times.


Known issues
------------

* Transactions should be atomic
    See: https://docs.djangoproject.com/en/1.7/topics/db/transactions/#django.db.transaction.non_atomic_requests
* Supports Python 2.7 and Django 1.7 only
