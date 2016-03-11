# coding: utf-8
from __future__ import unicode_literals

from django.db import models


class Compare(models.Model):
    time = models.DateTimeField(blank=False, auto_now=True, verbose_name='时间')

    def __unicode__(self):
        urls = []
        for item in self.loadresult_set.all():
            urls.append('[' + item.url + ']')
        return ' VS '.join(urls)

    class Meta:
        verbose_name = verbose_name_plural = '页面加载比较'


class LoadResult(models.Model):
    time = models.DateTimeField(blank=False, auto_now=True, verbose_name='时间')
    url = models.CharField(blank=False, max_length=100, verbose_name='地址')
    result = models.TextField(blank=False, verbose_name='加载结果json')
    compare = models.ForeignKey(Compare, on_delete=models.CASCADE, verbose_name='相关比较')

    def __unicode__(self):
        return '%s-%s' % (self.time, self.url)

    class Meta:
        verbose_name = verbose_name_plural = '页面统计结果'
