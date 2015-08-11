# -*- coding: utf-8 -*-

from __future__ import unicode_literals

#
# The sample_project.settings imports 'djmercadopago_sample_app_settings'.
#
# You can copy this file (remove '.SAMPLE' from its name)
#  to customize the settings of the sample app.
#
# The file 'djmercadopago_sample_app_settings.py' is ignored by Git to
#  avoid uploading your MercadoPago's settings by mistake.
#

DJMERCADOPAGO = {
    'CLIENT_ID': 'your-mp-client-id',
    'CLIENTE_SECRET': 'your-mp-secret',
    'SANDBOX_MODE': True,
    'CHECKOUT_PREFERENCE_UPDATER_FUNCTION':
        'sample_app.models.update_checkout_preference',
}
