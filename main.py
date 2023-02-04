from vk import VK
from yandex import Yandex
import configparser
import json
import tqdm

config = configparser.ConfigParser()
config.read('config.ini')

vk = VK(config['Authorization']['vk_token'])
ya = Yandex(config['Authorization']['ya_token'])


def upload_best_photos(user_id, n_best=5):
    path_ya = '/best_photos'
    ya.create_folder(path_ya)

    photos_info = vk.get_photos(user_id)['response']
    items_best = [dict()] * photos_info['count']
    n_best = min(n_best, photos_info['count'])

    for i, item in enumerate(photos_info['items']):
        best = max(item['sizes'], key=lambda e: e['height'] * e['width'])
        best['likes'] = item['likes']['count']
        best['date'] = item['date']
        items_best[i] = best

    items_best.sort(key=lambda e: e['height'] * e['width'])
    items_best = items_best[-n_best:]

    items_best.sort(key=lambda e: e['likes'])
    photos_info_out = [dict()] * len(items_best)
    for i, item in enumerate(tqdm.tqdm(items_best)):
        likes = item['likes']
        url = item['url']

        c1 = i > 0 and likes == items_best[i - 1]['likes']
        c2 = i < n_best - 1 and likes == items_best[i + 1]['likes']
        if c1 or c2:
            date = item['date']
            fname = f'{likes}_{date}.jpg'
        else:
            fname = f'{likes}.jpg'

        photos_info_out[i] = {'file_name': fname, 'size': item['type']}
        ya.upload_file_by_link(path_ya, url, fname)

    path_local = './'
    out_name = 'photos_info.json'
    with open(path_local + out_name, 'w') as out:
        json.dump(photos_info_out, out, indent=4)

    ya.upload_file_local(path_ya, path_local, out_name)


# shamrin_stas
# 72970028

def main():
    while True:
        try:
            user_id = input('Введите свой ID: ').replace(' ', '')
            if not user_id.isdigit():
                user_id = vk.resolve_screen_name(user_id)['response']['object_id']
            break
        except TypeError:
            print('Проверьте правильность ввода ID')

    n_best = int(input('Введите количество фотографий: ').replace(' ', ''))
    upload_best_photos(user_id, n_best=n_best)


if __name__ == '__main__':
    main()
