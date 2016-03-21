# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page_load', '0003_auto_20160317_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loadresult',
            name='doc',
        ),
    ]
