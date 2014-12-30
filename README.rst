=============
djmercadopago
=============

djmercadopago is a simple Django app to use MercadoPago

Quick start
-----------

1. Add "djmercadopago" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'djmercadopago',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^mp/', include('djmercadopago.urls')),

3. Run `python manage.py migrate` to create the polls models.
