# coding: utf-8
import json
from threading import Thread

from django.http.response import HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect

from .utils import load_page, analyse_load_result_with_cache, get_init_result, get_init_combined_result, combine_result
from .models import LoadResult, Compare


def load_page_by_thread(urls):
    load_results = {}
    threads = []

    def load_page_thread_target(url):
        load_result = load_page(url)
        if not load_result:
            load_result = load_page(url)
        load_results[url] = load_result

    for url in urls:
        load_results[url] = {}
        thread = Thread(target=load_page_thread_target, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return load_results


@require_POST
def analyse_page(request):
    urls = request.POST.getlist('url')
    if not urls:
        return HttpResponse('url is empty')

    load_results = load_page_by_thread(urls)

    cp = Compare()
    cp.save()
    for url in urls:
        load_result = load_results[url]['hars']
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
            urls.append({'url': load_result.url, 'id': load_result.id})
            json_result = json.loads(load_result.result)
            if not json_result:
                analyse_result_without_cache = get_init_result()
                analyse_result_with_cache = get_init_result()
            else:
                analyse_result_without_cache, analyse_result_with_cache = analyse_load_result_with_cache(json_result, load_result.url)
            combine_result(result, analyse_result_without_cache)
            combine_result(result, analyse_result_with_cache)
        context = {}
        context['result'] = result
        context['urls'] = urls
        context['object'] = self.object
        return context


def load_result(request, load_id):
    try:
        load = LoadResult.objects.get(pk=load_id)
    except LoadResult.DoesNotExist:
        raise Http404('load result %s' % load_id)
    url = load.url
    urls = [url]
    load_results = load_page_by_thread(urls)
    return HttpResponse(load_results[url]['content'])
