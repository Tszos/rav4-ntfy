import pytest
import requests

from carwatch.net import HostDown, RetrySession


class FakeResp:
    def __init__(self, status):
        self.status_code = status


def make(monkeypatch, outcomes):
    """Sesja, której kolejne zapytania zwracają/rzucają elementy z outcomes."""
    sleeps = []
    s = RetrySession(delays=(10, 30, 90), sleep=sleeps.append)
    it = iter(outcomes)

    def fake(self, method, url, *a, **kw):
        o = next(it)
        if isinstance(o, Exception):
            raise o
        return FakeResp(o)

    monkeypatch.setattr(requests.Session, "request", fake)
    return s, sleeps


def test_retries_with_growing_delays_then_succeeds(monkeypatch):
    s, sleeps = make(monkeypatch, [requests.exceptions.SSLError("tls"), 500, 200])
    assert s.get("https://a.pl/x").status_code == 200
    assert sleeps == [10, 30]


def test_no_retry_on_404(monkeypatch):
    s, sleeps = make(monkeypatch, [404])
    assert s.get("https://a.pl/x").status_code == 404
    assert sleeps == []


def test_host_marked_down_after_exhausting_retries(monkeypatch):
    s, sleeps = make(monkeypatch, [500, 500, 500, 503, 200])
    assert s.get("https://a.pl/x").status_code == 503
    assert sleeps == [10, 30, 90]
    with pytest.raises(HostDown):
        s.get("https://a.pl/y")
    assert s.get("https://b.pl/").status_code == 200  # inne hosty działają dalej
