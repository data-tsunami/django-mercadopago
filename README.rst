=============
djmercadopago
=============

djmercadopago is a simple Django app to use MercadoPago

THIS IS WIP. THIS DOESN'T WORK YET.

PLEASE, THINK TWICE BEFORE USING THIS ON A PRODUCTION ENVIRONMENT.

Most important things to do:

* document security issues
* implement exception handling
* more functional tests

Quick start
-----------

1. Add "djmercadopago" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'djmercadopago',
    )

2. Include the djmercadopago URLconf in your project urls.py like this::

    url(r'^mp/', include('djmercadopago.urls', namespace="djmercadopago")),

3. Connect to the 'checkout_preferences_created' signal, to update the **checkout preferences**::

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

    <a href="{% url 'djmercadopago:checkout' 'USER_CHECKOUT_IDENTIFIER' %}">Checkout</a>


The ``USER_CHECKOUT_IDENTIFIER`` is some identifier of the shopping cart, or purchase order, or whatever you
use to hold the items the user wants to pay. This identifier is passed to the function that populates
the ``checkout preferences`` dict, so you can query the database using that identifier.

If you have the shopping cart contents in session, you won't need an identifier.

Security considerations: since this identifier is used in an URL, anyone can try to guess it. If the identifier
is the ID of some database model, the function that handles the ``checkout_preferences_created``
signal should check the logged in user has permission to see that shopping cart / purchase order / etc.

Signal: checkout_preferences_created
------------------------------------

This signal is dispatched after the `checkout_preferences` dict is created, and before calling
the MP api. This allow the user of django-mercadopago to:

* add items and prices
* set `external reference`
* add back-urls

Other tasks to do in this signal handler:

* update any other `checkout_preferences` parameter
* validate user permissions
* create / update any of your models
* etc


When the ``checkout_preferences_created`` signal is sent, 3 parameters are provided:

* checkout_preferences
* user_checkout_identifier
* request

The recommended way to use it is to connect to the signals in the ``models.py`` module::

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

For example, to set the successful url::

    back_urls = checkout_preferences.get('back_urls', {})
    checkout_preferences['back_urls'] = back_urls
    back_urls['success'] = request.build_absolute_uri(reverse('successful_checkout'))

For example, to set the ``items`` to purchase, and the ``external_reference``::

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


Parameters
==========

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
* get the User (for example, to validate that the current user is the owner of the
  items identified by ``user_checkout_identifier``)


Payment model
-------------

Before calling MP API, an instance of ``Payment`` is created. The same instances is
updated with the response received from MP. In the instance, the ``external_reference``
is saved (if you added it to the ``checkout preferences``) to allow you to track payments.

If you need to persist a reference to the ``Payment`` instance, you can register
to the post_save signal of the model (see:
https://docs.djangoproject.com/en/1.7/ref/signals/#django.db.models.signals.post_save ).

The signal will be generated twice, since save() is called two times.


Known issues
------------

* Transactions should be atomic
    See: https://docs.djangoproject.com/en/1.7/topics/db/transactions/#django.db.transaction.non_atomic_requests
* Supports Python 2.7 and Django 1.7 only
