# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page_load', '0002_loadresult_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadresult',
            name='url',
            field=models.CharField(max_length=1000, verbose_name='\u5730\u5740'),
        ),
    ]
