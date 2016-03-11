# coding: utf-8
import subprocess
import json
import re
import os


def load_page(url):
    js_file = os.path.join(os.path.dirname(__file__), 'netsniff.js')
    try:
        output = subprocess.check_output(['phantomjs', js_file, url])
    except subprocess.CalledProcessError:
        return None
    output = output.split('xafexdfea980!adaf*>M')
    if len(output) == 1:
        return None
    output = output[1]
    try:
        return json.loads(output)
    except ValueError:
        return None


def add_entry(entry, field, final_result):
    final_result['size'][field] += entry['response']['bodySize']
    final_result['size']['all'] += entry['response']['bodySize']
    final_result['count'][field] += 1
    final_result['count']['all'] += 1


def check_request(field, regstr, entry, final_result):
    url = entry['request']['url']
    m = re.match(regstr, url)
    if m:
        add_entry(entry, field, final_result)
        return True
    return False


def get_init_result():
    final_result = {
        'size': {
            'doc': 0.0,
            'js': 0.0,
            'css': 0.0,
            'img': 0.0,
            'other': 0.0,
            'all': 0.0,
        },
        'count': {
            'js': 0,
            'css': 0,
            'img': 0,
            'other': 0,
            'all': 0
        },
        'load_complete_time': 0.0
    }
    return final_result


def get_init_combined_result():
    combined_result = {
        'size': {
            'doc': [],
            'js': [],
            'css': [],
            'img': [],
            'other': [],
            'all': [],
        },
        'count': {
            'js': [],
            'css': [],
            'img': [],
            'other': [],
            'all': []
        },
        'load_complete_time': []
    }
    return combined_result


def analyse_load_result(result, url):
    final_result = get_init_result()
    final_result['load_complete_time'] = result['log']['pages'][0]['pageTimings']['onLoad']
    entries = result['log']['entries']
    for entry in entries:
        entry_url = entry['request']['url']
        if entry_url == url:
            final_result['size']['doc'] += entry['response']['bodySize']
        if check_request('js', r'.*\.js$', entry, final_result):
            continue
        elif check_request('css', r'.*\.css$', entry, final_result):
            continue
        elif check_request('img', r'.*\.(png|jpg|jpeg|gif|ico|webp)$', entry, final_result):
            continue
        else:
            add_entry(entry, 'other', final_result)
    return final_result


def combine_result(combined, result):
    combined['load_complete_time'].append(result['load_complete_time'])
    combined['size']['doc'].append(result['size']['doc'])
    combined['size']['js'].append(result['size']['js'])
    combined['size']['css'].append(result['size']['css'])
    combined['size']['img'].append(result['size']['img'])
    combined['size']['other'].append(result['size']['other'])
    combined['size']['all'].append(result['size']['all'])
    combined['count']['js'].append(result['count']['js'])
    combined['count']['css'].append(result['count']['css'])
    combined['count']['img'].append(result['count']['img'])
    combined['count']['other'].append(result['count']['other'])
    combined['count']['all'].append(result['count']['all'])



if __name__ == '__main__':
    source = load_page('http://m.sohu.com/?v=3')
    # if source:
    #     print analyse_load_result(source, 'http://xw.qq.com/index.htm')
