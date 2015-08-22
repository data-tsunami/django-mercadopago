# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import dispatch


checkout_preferences_created = dispatch.Signal(providing_args=["checkout_preferences",
                                                               "user_checkout_identifier",
                                                               "request"])
