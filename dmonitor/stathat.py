import requests


class StatHat:
    api_base = 'https://api.stathat.com/'

    def __init__(self, key: str):
        self.key = key
        self.session = requests.Session()

    def request(self, path: str, data: dict) -> str:
        response = self.session.post(self.api_base + path, data=data)
        response.raise_for_status()
        return response.text

    def post_value(self, stat_name: str, value: float, timestamp: int = None):
        args = {'ezkey': self.key, 'stat': stat_name, 'value': value}
        if timestamp is not None:
            args['t'] = timestamp
        return self.request('ez', args)

    def post_count(self, stat_name: str, count: int, timestamp: int = None):
        args = {'ezkey': self.key, 'stat': stat_name, 'count': count}
        if timestamp is not None:
            args['t'] = timestamp
        return self.request('ez', args)
