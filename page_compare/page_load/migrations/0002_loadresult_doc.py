# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page_load', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadresult',
            name='doc',
            field=models.TextField(default='', verbose_name='\u6587\u6863\u9875\u9762'),
            preserve_default=True,
        ),
    ]
