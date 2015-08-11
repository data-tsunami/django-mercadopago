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

3. Implement the function that populates the **checkout preferences** dict::

    url(r'^mp/', include('djmercadopago.urls', namespace="djmercadopago")),


4. Configure your settings::

    DJMERCADOPAGO = {
        'CLIENT_ID': 'YOUR-MERCADOPAGO-CLIENT-ID',
        'CLIENT_SECRET': 'YOUR-MERCADOPAGO-SECRET',
        'SANDBOX_MODE': True,
        'CHECKOUT_PREFERENCE_UPDATER_FUNCTION': 'package.module.to.your.function.defined.in.step.three',
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

You can name this function whatever you want, but you need to receive 3 parameters::

    def sample_update_checkout_preference(checkout_preference, checkout_identifier, request):
        (...)

This function is configured in the settings file, in the
variable 'DJMERCADOPAGO', with key 'CHECKOUT_PREFERENCE_UPDATER_FUNCTION'::

    DJMERCADOPAGO = {

        (...)

        'CHECKOUT_PREFERENCE_UPDATER_FUNCTION':
            'MYAPP.MYMODULE.sample_update_checkout_preference',
    }


Parameter: checkout_preference
******************************

Dictionary with the checkout preferences to call the MP api.
You need to populate this object with the required information,
including items, back urls, etc.

Parameter: checkout_identifier
******************************

The same string used when created the link to the ``djmercadopago:checkout`` view.

Example: if the URL was generated with::

   {% url 'djmercadopago:checkout' purchase_order.id %}

the value of ``checkout_identifier`` would be the value of ``purchase_order.id``

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
https://docs.djangoproject.com/en/1.7/ref/signals/#django.db.models.signals.post_save )



Known issues
------------

* Transactions should be atomic
    See: https://docs.djangoproject.com/en/1.7/topics/db/transactions/#django.db.transaction.non_atomic_requests
* Supports Python 2.7 and Django 1.7 only
