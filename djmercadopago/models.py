# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Payment(models.Model):
    # payment_id = models.BigIntegerField(null=True)
    checkout_preferences = models.TextField()
    checkout_response = models.TextField()
    external_reference = models.TextField()
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)
