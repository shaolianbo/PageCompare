from django.conf.urls import patterns, include, url
from django.contrib import admin

from page_load.views import analyse_page, CompareList, CompareDetail, load_result
from page_load.models import Compare

# admin.site.register(LoadResult)
admin.site.register(Compare)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'page_compare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^run/', analyse_page),
    url(r'^load_compare/', CompareList.as_view()),
    url(r'^compare_detail/(?P<pk>[0-9]+)/$', CompareDetail.as_view()),
    url(r'^load_result/(\d+)/$', load_result),
)
