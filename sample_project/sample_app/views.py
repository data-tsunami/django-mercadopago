# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.views.generic.base import TemplateView

from sample_app import models


class HomeView(TemplateView):
    template_name = 'sample_app/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['product_list'] = models.PRODUCT_LIST
        return ctx


class SuccessfulCheckoutView(TemplateView):
    template_name = 'sample_app/success.html'
    pass
