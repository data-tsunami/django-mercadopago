# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djmercadopago', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='external_reference',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
