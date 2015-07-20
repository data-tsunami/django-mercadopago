# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
BASE_DIR = os.path.dirname(__file__)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'djmercadopago',
)

SECRET_KEY = '0123456789'
