# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, verbose_name='\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u9875\u9762\u52a0\u8f7d\u6bd4\u8f83',
                'verbose_name_plural': '\u9875\u9762\u52a0\u8f7d\u6bd4\u8f83',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoadResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, verbose_name='\u65f6\u95f4')),
                ('url', models.CharField(max_length=100, verbose_name='\u5730\u5740')),
                ('result', models.TextField(verbose_name='\u52a0\u8f7d\u7ed3\u679cjson')),
                ('compare', models.ForeignKey(verbose_name='\u76f8\u5173\u6bd4\u8f83', to='page_load.Compare')),
            ],
            options={
                'verbose_name': '\u9875\u9762\u7edf\u8ba1\u7ed3\u679c',
                'verbose_name_plural': '\u9875\u9762\u7edf\u8ba1\u7ed3\u679c',
            },
            bases=(models.Model,),
        ),
    ]
