# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'sample_app/index.html'
