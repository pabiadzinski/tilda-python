#!/usr/bin/python

import os
import requests
import argparse
from dotenv import load_dotenv
import time

from tildaapi import Client

load_dotenv()

PUBLIC_KEY = os.getenv("TILDA_PUBLIC_KEY")
SECRET_KEY = os.getenv("TILDA_SECRET_KEY")
PROJECT_ID = os.getenv("TILDA_PROJECT_ID")

DEFAULT_SYMLINK = os.path.abspath('../tildastatic')
DATETIME = time.strftime('%Y%m%d-%H%M%S')
DESTINATION_FOLDER = os.path.abspath('tilda_' + DATETIME + '/') + '/'

FOLDERS = {
    'js': DESTINATION_FOLDER + 'js/',
    'css': DESTINATION_FOLDER + 'css/',
    'images': DESTINATION_FOLDER + 'images/',
}


def create_root_folder(folder):
    if os.path.exists(folder):
        pass
    else:
        os.mkdir(folder)


def prepare_dirs(folders):
    for key, path in folders.items():
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)


def save_file(content, filename):
    with open(filename, 'w') as handler:
        handler.write(content)


def download_file(path, filename):
    data = requests.get(path).content
    with open(filename, 'wb') as handler:
        handler.write(data)


def save_assets(data, folders):
    for row in data['css']:
        download_file(row['from'], folders['css'] + row['to'])
        log('Downloaded css: ', row['from'])

    for row in data['js']:
        download_file(row['from'], folders['js'] + row['to'])
        log('Downloaded js: ', row['from'])

    for row in data['images']:
        download_file(row['from'], folders['images'] + row['to'])
        log('Downloaded image: ', row['from'])

    save_file(data['htaccess'], '.htaccess')


def log(text, value=None):
    print(text, value)


def create_symlink(src_path):
    if os.path.islink(src_path):
        os.remove(src_path)

    os.symlink(DESTINATION_FOLDER, src_path)


def export():
    client = Client(SECRET_KEY, PUBLIC_KEY)

    prepare_dirs(FOLDERS)

    project_data = client.get_project_export(PROJECT_ID)

    save_assets(project_data, FOLDERS)

    pages_data = client.get_pages_list(PROJECT_ID)

    for page in pages_data:
        page_info = client.get_page_full_export(page['id'])
        save_file(page_info['html'], DESTINATION_FOLDER + page_info['filename'])

        for image in page_info['images']:
            download_file(image['from'], FOLDERS['images'] + image['to'])
            log('Downloaded image: ', image['from'])


if __name__ == '__main__':
    create_root_folder(DESTINATION_FOLDER)

    export()

    log("EXPORT DONE")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--symlink_path', '-sp', default=DEFAULT_SYMLINK, help='destination folder (default: ' + DEFAULT_SYMLINK + ')'
    )

    args = parser.parse_args()
    symlink_path = args.symlink_path

    create_symlink(symlink_path)

    log("SYMLINK CREATED")
