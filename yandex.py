import requests
import time


class Yandex:
    host = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def delete_folder(self, path):
        uri = '/v1/disk/resources'
        url = self.host + uri
        params = {'path': path}
        res = requests.delete(url, headers=self.get_headers(), params=params)

        return res.status_code

    def create_folder(self, path):
        uri = '/v1/disk/resources'
        url = self.host + uri
        params = {'path': path}
        self.delete_folder(path)

        while requests.get(url, headers=self.get_headers(), params=params).status_code != 404:
            time.sleep(1)

        res = requests.put(url, headers=self.get_headers(), params=params)

        return res.status_code

    def upload_file_by_link(self, path_ya, file_link, file_name):
        uri = '/v1/disk/resources/upload'
        url = self.host + uri
        params = {'path': f'{path_ya}/{file_name}', 'url': file_link}
        res = requests.post(url, headers=self.get_headers(), params=params)

        return res.status_code

    def upload_file_local(self, path_ya, path_local, file_name):
        uri = '/v1/disk/resources/upload'
        url = self.host + uri

        params = {'path': f'{path_ya}/{file_name}'}
        res = requests.get(url, headers=self.get_headers(), params=params).json()
        upload_link = res['href']

        res = requests.put(upload_link, headers=self.get_headers(), data=open(path_local + file_name, 'rb'))

        return res.status_code
