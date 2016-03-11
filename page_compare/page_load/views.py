# coding: utf-8
import json

from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect

from .utils import load_page, analyse_load_result, get_init_result, get_init_combined_result, combine_result
from .models import LoadResult, Compare


@require_POST
def analyse_page(request):
    urls = request.POST.getlist('url')
    if not urls:
        return HttpResponse('url is empty')
    cp = Compare()
    cp.save()
    for url in urls:
        load_result = load_page(url) or {}
        if not load_result:
            load_result = load_page(url) or {}
        db_load_result = LoadResult(url=url, result=json.dumps(load_result), compare=cp)
        db_load_result.save()
    return redirect('/compare_detail/%s/' % cp.id)


class CompareList(ListView):
    model = Compare
    queryset = Compare.objects.all().order_by("-time")


class CompareDetail(DetailView):
    model = Compare

    def get_context_data(self, *args, **kwargs):
        load_results = self.object.loadresult_set.all()
        result = get_init_combined_result()
        urls = []
        for load_result in load_results:
            urls.append(load_result.url)
            json_result = json.loads(load_result.result)
            if not json_result:
                analyse_result = get_init_result()
            else:
                analyse_result = analyse_load_result(json_result, load_result.url)
            combine_result(result, analyse_result)
        context = {}
        context['result'] = result
        context['urls'] = urls
        context['object'] = self.object
        return context
