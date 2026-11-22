"""Pobieranie ofert używanych RAV4 z pewneauto.pl (salony z config.DEALERS)."""

import re
from dataclasses import asdict, dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from carwatch import config


@dataclass
class Offer:
    id: str
    dealer: str
    title: str
    year: int | None
    mileage_km: int | None
    fuel: str
    price: int | None
    url: str
    image: str | None
    station_id: int | None = None  # ID salonu (config.DEALERS)

    def to_dict(self) -> dict:
        return asdict(self)


def _digits(text: str | None) -> int | None:
    if not text:
        return None
    d = re.sub(r"\D", "", text)
    return int(d) if d else None


def parse_listing(html: str, dealer: str, base_url: str = config.USED_BASE_URL) -> list[Offer]:
    soup = BeautifulSoup(html, "html.parser")
    offers = []
    for box in soup.select("div.o-bx[offer-id]"):
        link = box.select_one(".o-bx__title a") or box.select_one("a[href]")
        subtitle = box.select_one(".o-bx__title span")
        info = [li.get_text(" ", strip=True) for li in box.select(".o-bx__info li")]
        year = next((int(x) for x in info if re.fullmatch(r"(19|20)\d{2}", x)), None)
        mileage = next((_digits(x) for x in info if x.endswith("km")), None)
        fuel_el = box.select_one(".o-bx__info [class*=color-]")
        price_el = box.select_one(".retail-price strong")
        img = box.select_one(".o-bx__gallery img")
        offers.append(
            Offer(
                id=box["offer-id"],
                dealer=dealer,
                title=(subtitle.get_text(" ", strip=True) if subtitle else "Toyota RAV4"),
                year=year,
                mileage_km=mileage,
                fuel=fuel_el.get_text(strip=True) if fuel_el else "",
                price=_digits(price_el.get_text() if price_el else None),
                url=urljoin(base_url, link["href"]) if link else base_url,
                image=img.get("src") if img else None,
            )
        )
    return offers


def matches(offer: Offer) -> bool:
    return (
        offer.year is not None
        and offer.year >= config.MIN_YEAR
        and offer.fuel in config.ALLOWED_FUELS
    )


def fetch_listing(session: requests.Session, base_url: str, params: dict, dealer: str,
                  max_pages: int = config.MAX_PAGES) -> list[Offer]:
    """Wszystkie strony listingu RAV4 dla podanych filtrów (bez filtrowania lokalnego)."""
    url = base_url + config.USED_LISTING_PATH
    found: dict[str, Offer] = {}
    for page in range(1, max_pages + 1):
        query = dict(params)
        if page > 1:
            query["strona"] = page
        resp = session.get(url, params=query, headers=config.HEADERS, timeout=30)
        resp.raise_for_status()
        new = [o for o in parse_listing(resp.text, dealer, base_url) if o.id not in found]
        if not new:
            break
        found.update((o.id, o) for o in new)
        if f"strona={page + 1}" not in resp.text:
            break
    return list(found.values())


def fetch_dealer_offers(session: requests.Session, station_id: int, dealer: str) -> list[Offer]:
    params = {"station-id": station_id, "year-from": config.MIN_YEAR}
    offers = [o for o in fetch_listing(session, config.USED_BASE_URL, params, dealer) if matches(o)]
    for o in offers:
        o.station_id = station_id
    return offers


def fetch_all(session: requests.Session) -> list[Offer]:
    offers: dict[str, Offer] = {}
    for station_id, dealer in config.DEALERS.items():
        for o in fetch_dealer_offers(session, station_id, dealer):
            offers.setdefault(o.id, o)
    return list(offers.values())


def listing_url() -> str:
    """Link do listingu RAV4 ze wszystkich obserwowanych salonów."""
    ids = ",".join(str(i) for i in config.DEALERS)
    return (f"{config.USED_BASE_URL}{config.USED_LISTING_PATH}"
            f"?station-id={ids}&year-from={config.MIN_YEAR}")


def fetch_market(session: requests.Session) -> list[Offer]:
    """RAV4 z całej Polski (program Toyota Pewne Auto) – do porównania cen."""
    offers: list[Offer] = []
    for fuel in config.ALLOWED_FUELS:
        param = config.MARKET_FUEL_PARAMS.get(fuel)
        if not param:
            continue
        params = {"year-from": config.MIN_YEAR, "fuel": param}
        offers.extend(fetch_listing(session, config.MARKET_BASE_URL, params, "",
                                    config.MARKET_MAX_PAGES))
    return [o for o in offers if matches(o)]
