import ipaddress
import os
import sys
import time
from enum import Enum
from pathlib import Path
from typing import Optional

import requests

if sys.platform != 'win32':
    import fcntl


class IPNetworks(Enum):
    umos = (
        ipaddress.ip_network('85.89.126.0/23'),
    )
    imt = (
        ipaddress.ip_network('45.147.81.0/24'),
        ipaddress.ip_network('45.147.82.0/23'),
        ipaddress.ip_network('212.16.0.0/19'),
        ipaddress.ip_network('212.16.0.0/20'),
        ipaddress.ip_network('212.16.16.0/20'),
        ipaddress.ip_network('212.16.16.0/21'),
        ipaddress.ip_network('212.16.24.0/22'),
    )

    @classmethod
    def provider(cls, ip: ipaddress.IPv4Address) -> Optional[str]:
        for provider in cls:
            for network in provider.value:
                if ip in network:
                    return provider.name
        return None


class CheckMyIP:
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

    def provider(self) -> Optional[str]:
        ip = self.get_ip()
        if ip is None:
            return None
        return IPNetworks.provider(ip)


class Timer:
    def __init__(self, interval: float):
        self.interval = float(interval)
        self.last = 0.

    def start(self):
        self.last = time.monotonic()
        return self

    def reset(self):
        self.last = 0
        return self

    def acquire(self):
        curr_ts = time.monotonic()
        if self.last + self.interval > curr_ts:
            return False
        self.last = curr_ts
        return True


class SingleInstance:
    def __init__(self, lock_file: Path = None):
        self.locked = False
        self.lock_file = lock_file or project_path('lock')
        self.fd = None

    def try_lock(self) -> bool:
        if sys.platform == 'win32':
            try:
                self.lock_file.unlink(missing_ok=True)
                self.fd = os.open(str(self.lock_file), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except OSError:
                return False

        else:
            self.fd = self.lock_file.open('w')
            self.fd.flush()
            try:
                fcntl.lockf(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                return False

        self.locked = True
        return True

    def unlock(self):
        if not self.locked:
            return

        if sys.platform != 'win32':
            fcntl.lockf(self.fd, fcntl.LOCK_UN)

        if self.fd:
            os.close(self.fd)

        self.lock_file.unlink(missing_ok=True)
        self.locked = False

    def __del__(self):
        self.unlock()


def project_path(name: str) -> Path:
    file = Path.home() / Path(f'.dmonitor/{name}')
    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch()
    return file
