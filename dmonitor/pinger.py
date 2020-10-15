import json
import time
from typing import Tuple

import ping3

import config
from stathat import StatHat
from utils import project_path


class Pinger:
    def __init__(self, stathat: StatHat):
        self.stathat = stathat
        self.data = {}
        self.data_file = project_path('data.json')
        self.load()

    def load(self):
        try:
            self.data = json.loads(self.data_file.read_text(encoding='utf-8'))
        except json.decoder.JSONDecodeError:
            self.data = {}

    def dump(self):
        self.data_file.write_text(json.dumps(self.data), encoding='utf-8')

    @staticmethod
    def key(ts: int = None) -> str:
        ts = int(ts or time.time())
        return str(ts - ts % 60)

    @staticmethod
    def ping() -> Tuple[dict, bool]:
        data = {'avg': 0., 'downtime': False}

        delays = []
        for domain in config.domains:
            delay = ping3.ping(domain, unit='ms')
            if delay is None:
                data['downtime'] = True
            else:
                delays.append(delay)

        data['avg'] = sum(delays) / len(delays) if delays else 60_000
        return data, data['downtime']

    def upload_metrics(self):
        try:
            for k, v in self.data.items():
                if v.get('downtime'):
                    self.stathat.post_count('msu - downtime', 1, timestamp=int(k))
                self.stathat.post_count('msu - submissions', 1, timestamp=int(k))
                self.stathat.post_value('msu - avg ping', v['avg'], timestamp=int(k))
        except Exception:
            pass
        else:
            self.data.clear()

    def analyze(self):
        key = self.key()

        data, downtime = self.ping()
        self.data[key] = data

        if not downtime:
            self.upload_metrics()

        self.dump()
        return not downtime
