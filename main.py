import requests

from Yandex_Token import Token
from VK_Token import vk_token


class Yandex:
    host = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folder(self):
        uri = '/v1/disk/resources'
        url = self.host + uri
        params = {'path': '/new_folder'}
        requests.put(url, headers=self.get_headers(), params=params)

    def upload_file(self, file_link, file_name):
        uri = '/v1/disk/resources/upload'
        url = self.host + uri
        params = {'path': f'/new_folder/{file_name}', 'url': file_link}
        res = requests.post(url, headers=self.get_headers(), params=params)
        if res.status_code in (200, 202):
            print('Фотография загружена')
        else:
            print('Ошибка загрузки')


class VK:
    host = 'https://api.vk.com/method'

    def __init__(self, token):
        self.token = token

    def get_photos(self, user_id):
        uri = '/photos.get'
        url = self.host + uri
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'access_token': self.token,
            'v': '5.131',
            'extended': '1',
            'photo_sizes': '1'
        }
        res = requests.get(url, params). json()
        return res


def upload_best_photos(user_id, n_best=5):
    vk = VK(vk_token)
    photos_info = vk.get_photos(user_id)['response']
    items_best = [0] * photos_info['count']
    n_best = min(n_best, photos_info['count'])

    for i, item in enumerate(photos_info['items']):
        best = max(item['sizes'], key=lambda e: e['height'] * e['width'])
        best['likes'] = item['likes']['count']
        items_best[i] = best

    items_best.sort(key=lambda e: e['height'] * e['width'])
    for item in items_best[-n_best:]:
        likes = item['likes']
        url = item['url']

        ya = Yandex(Token)
        ya.create_folder()
        ya.upload_file(url, f'{likes}.jpg')


def main():
    user_id = input('Введите свой ID: ')
    upload_best_photos(user_id)


main()
