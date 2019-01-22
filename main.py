#!/usr/bin/python

import requests
import urllib.parse
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_HOST = 'http://api.tildacdn.info/v1/'

PUBLIC_KEY = os.getenv("TILDA_PUBLIC_KEY")
PRIVATE_KEY = os.getenv("TILDA_PRIVATE_KEY")
PROJECT_ID = os.getenv("TILDA_PROJECT_ID")


METHODS = {
    'GET_PAGE_FULL_EXPORT': 'getpagefullexport',
    'GET_PROJECT_EXPORT': 'getprojectexport',
    'GET_PAGES_LIST': 'getpageslist',
}

FOLDERS = {
    'js': './js/',
    'css': './css/',
    'images': './images/'
}


def prepare_dirs():
    for key, path in FOLDERS.items():
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)


def check_response_status(data):
    if data['status'] == 'FOUND':
        return True

    return False


def get_api_url(method):
    params = {
        'publickey': PUBLIC_KEY,
        'secretkey': PRIVATE_KEY,
        'projectid': PROJECT_ID
    }

    return API_HOST + method + "/?" + urllib.parse.urlencode(params)


def get_page_url(page):
    params = {
        'publickey': PUBLIC_KEY,
        'secretkey': PRIVATE_KEY,
        'pageid': page
    }

    return API_HOST + METHODS['GET_PAGE_FULL_EXPORT'] + "/?" + urllib.parse.urlencode(params)


def get_project_export():
    data = do_request(METHODS['GET_PROJECT_EXPORT'])

    return data


def save_static_files(data):
    for row in data['result']['css']:
        print('Downloaded css: ', row['from'])
        download_file(row['from'], FOLDERS['css'] + row['to'])

    for row in data['result']['js']:
        print('Downloaded js: ', row['from'])
        download_file(row['from'], FOLDERS['js'] + row['to'])

    for row in data['result']['images']:
        print('Downloaded image: ', row['from'])
        download_file(row['from'], FOLDERS['images'] + row['to'])

    save_file(data['result']['htaccess'], '.htaccess')
    print('Downloaded htaccess')


def get_pages_list():
    return do_request(METHODS['GET_PAGES_LIST'])


def get_page_full_export(id):
    page = get_page(id)

    if check_response_status(page):
        save_file(page['result']['html'], page['result']['filename'])
    else:
        print(page['message'])

    return page


def download_file(path, filename):
    data = requests.get(path).content
    with open(filename, 'wb') as handler:
        handler.write(data)


def do_request(method):
    url = get_api_url(method)
    response = requests.get(url)

    return json.loads(response.content)


def get_page(page):
    url = get_page_url(page)
    response = requests.get(url)

    return json.loads(response.content)


def save_file(content, filename):
    with open('./' + filename, 'w') as handler:
        handler.write(content)


def main():
    prepare_dirs()

    project = get_project_export()

    if check_response_status(project):
        save_static_files(project)

        pages = get_pages_list()

        if check_response_status(pages):
            for page in pages['result']:
                page_info = get_page_full_export(page['id'])

                for row in page_info['result']['images']:
                    print('Downloaded page image: ', row['from'])
                    download_file(row['from'], FOLDERS['images'] + row['to'])
        else:
            print(pages['message'])

    else:
        print(project['message'])


if __name__ == '__main__':
    main()
