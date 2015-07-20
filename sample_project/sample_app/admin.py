# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from djmercadopago import models


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('external_reference', 'creation_timestamp', 'last_update_timestamp')


admin.site.register(models.Payment, PaymentAdmin)
