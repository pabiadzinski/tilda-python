#!/usr/bin/python

import requests
import urllib.parse
import json
import os

API_HOST = 'http://api.tildacdn.info/v1/'

PUBLIC_KEY = ""
PRIVATE_KEY = ""
PROJECT_ID = ''


METHODS = (
    "methods",
)

FOLDERS = (
    './css',
    './js',
    './img'
)


def prepare_dirs():
    for f in FOLDERS:
        if os.path.exists(f):
            pass
        else:
            os.mkdir(f)


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

    return API_HOST + "getpagefullexport" + "/?" + urllib.parse.urlencode(params)


def get_project_export():
    data = do_request("getprojectexport")

    return data


def save_static_files(data):
    for row in data['result']['css']:
        print("Downloaded css: ", row['from'])
        download_file(row['from'], './css/' + row['to'])

    for row in data['result']['js']:
        print("Downloaded js: ", row['from'])
        download_file(row['from'], './js/' + row['to'])

    for row in data['result']['images']:
        print("Downloaded image: ", row['from'])
        download_file(row['from'], './img/' + row['to'])

    save_file(data["result"]["htaccess"], ".htaccess")
    print("Downloaded htaccess")


def get_pages_list():
    return do_request("getpageslist")


def get_page_full_export(id):
    page = get_page(id)

    if check_response_status(page):
        save_file(page['result']['html'], page['result']['filename'])

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
    with open("./" + filename, 'w') as handler:
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

            for row in page_info["result"]['images']:
                print("Downloaded page image: ", row['from'])
                download_file(row['from'], './img/' + row['to'])


if __name__ == "__main__":
    main()
