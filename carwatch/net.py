"""Sesja HTTP, która ponawia zapytania przy chwilowych awariach stron.

Odstępy rosną wykładniczo (domyślnie 10 s, 30 s, 90 s), żeby leżąca strona miała czas wstać.
Gdy host nie odpowie po wszystkich próbach, kolejne zapytania do niego w tym uruchomieniu
padają od razu: inaczej kilkadziesiąt stron listingu przekroczyłoby limit czasu joba.
"""

import sys
import time
from urllib.parse import urlsplit

import requests

RETRY_DELAYS = (10, 30, 90)  # sekundy przed 2., 3. i 4. próbą
RETRY_STATUSES = {429, 500, 502, 503, 504}


class HostDown(requests.ConnectionError):
    """Host nie odpowiedział poprawnie po wszystkich próbach."""


class RetrySession(requests.Session):
    def __init__(self, delays: tuple[float, ...] = RETRY_DELAYS, sleep=time.sleep):
        super().__init__()
        self.delays = delays
        self.sleep = sleep
        self.down: set[str] = set()

    def request(self, method, url, *args, **kwargs):
        host = urlsplit(url).netloc
        if host in self.down:
            raise HostDown(f"{host} nie odpowiada (pominięto po wcześniejszych próbach)")
        for attempt, delay in enumerate((*self.delays, None), start=1):
            try:
                resp = super().request(method, url, *args, **kwargs)
            except (requests.ConnectionError, requests.Timeout) as e:  # SSLError też tu wpada
                if delay is None:
                    self.down.add(host)
                    raise
                problem = repr(e)
            else:
                if resp.status_code not in RETRY_STATUSES:
                    return resp
                if delay is None:
                    self.down.add(host)
                    return resp  # wywołujący i tak zrobi raise_for_status()
                problem = f"HTTP {resp.status_code}"
            print(f"{host}: {problem}; próba {attempt + 1} za {delay} s", file=sys.stderr)
            self.sleep(delay)
        raise AssertionError("nieosiągalne")
