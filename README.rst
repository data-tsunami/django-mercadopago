=============
djmercadopago
=============

djmercadopago is a simple Django app to use MercadoPago


THIS IS WIP. THIS DOESN'T WORK YET.


Quick start
-----------

1. Add "djmercadopago" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'djmercadopago',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^mp/', include('djmercadopago.urls', namespace="djmercadopago")),

3. Run `python manage.py migrate` to create the polls models.

4. In your template, add a link to the checkout view:

    <a href="{% url 'djmercadopago:checkout' 'some-item-id' %}">Checkout</a>

Known issues
------------

* Transactions should be atomic
    See: https://docs.djangoproject.com/en/1.7/topics/db/transactions/#django.db.transaction.non_atomic_requests
