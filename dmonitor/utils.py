import ipaddress
import time
from pathlib import Path
from typing import Optional

import requests


class CheckMyIP:
    ip_start = '85.89.126.0'
    ip_end = '85.89.127.255'

    def __init__(self):
        self.session = requests.Session()
        self.ip_file = project_path('ip.txt')

    def extract_ip(self) -> Optional[ipaddress.IPv4Address]:
        return self.parse_ip(self.ip_file.read_text(encoding='utf-8'))

    def request_ip(self) -> Optional[ipaddress.IPv4Address]:
        try:
            response = self.session.get('https://checkip.amazonaws.com')
            response.raise_for_status()
        except Exception:
            return None

        ip = self.parse_ip(response.text.strip())
        if ip is not None:
            self.ip_file.write_text(str(ip), encoding='utf-8')
        return ip

    @staticmethod
    def parse_ip(ip: str) -> Optional[ipaddress.IPv4Address]:
        try:
            ip = ipaddress.ip_address(ip)
        except ValueError:
            return None
        return ip

    def get_ip(self) -> Optional[ipaddress.IPv4Address]:
        ip = self.request_ip()
        if ip is None:
            ip = self.extract_ip()
            if ip is None:
                return None
        return ip

    def check(self) -> bool:
        ip = self.get_ip()
        if ip is None:
            return False
        return ipaddress.ip_address(self.ip_start) <= ip <= ipaddress.ip_address(self.ip_end)


class Timer:
    def __init__(self, interval: float):
        self.interval = float(interval)
        self.last = 0.

    def start(self):
        self.last = time.monotonic()
        return self

    def acquire(self):
        curr_ts = time.monotonic()
        if self.last + self.interval > curr_ts:
            return False
        self.last = curr_ts
        return True


def project_path(name: str) -> Path:
    file = Path.home() / Path(f'.dmonitor/{name}')
    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch()
    return file
