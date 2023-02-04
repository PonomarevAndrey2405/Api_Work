import requests


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
        res = requests.get(url, params).json()
        return res

    def resolve_screen_name(self, screen_name):
        uri = '/utils.resolveScreenName'
        url = self.host + uri
        params = {
            'screen_name': screen_name,
            'access_token': self.token,
            'v': '5.131'
        }
        res = requests.get(url, params).json()
        return res
