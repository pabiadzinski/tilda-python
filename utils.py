import os
import requests


class Utils(object):
    @staticmethod
    def prepare_dirs(folders):
        for key, path in folders.items():
            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)

    @staticmethod
    def save_file(content, filename):
        with open('./' + filename, 'w') as handler:
            handler.write(content)

    @staticmethod
    def download_file(path, filename):
        data = requests.get(path).content
        with open(filename, 'wb') as handler:
            handler.write(data)

    @staticmethod
    def save_assets(data, folders):
        for row in data['css']:
            print('Downloaded css: ', row['from'])
            Utils.download_file(row['from'], folders['css'] + row['to'])

        for row in data['js']:
            print('Downloaded js: ', row['from'])
            Utils.download_file(row['from'], folders['js'] + row['to'])

        for row in data['images']:
            print('Downloaded image: ', row['from'])
            Utils.download_file(row['from'], folders['images'] + row['to'])

        Utils.save_file(data['htaccess'], '.htaccess')
        print('Downloaded htaccess')
