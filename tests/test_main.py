from carwatch import main
from carwatch.used_offers import Offer


def _offer(i, station, price=150_000):
    dealer = main.config.DEALERS[station]
    return Offer(str(i), dealer, "2.5 Hybrid Comfort 4x4", 2023, 50_000, "Hybryda", price,
                 f"https://pewneauto.pl/oferta/toyota-rav4/{i}", None, station)


def _run(monkeypatch, state, offers):
    sent = []
    monkeypatch.setattr(main, "fetch_all", lambda session: offers)
    monkeypatch.setattr(main, "get_details", lambda ctx, o, prev: {})
    monkeypatch.setattr(main.notify, "send", lambda title, msg, **kw: sent.append((title, msg, kw)))
    ctx = main.Context(None)
    ctx._market = []
    main.check_used(ctx, state)
    return sent


def test_new_dealers_are_seeded_silently(monkeypatch):
    # stan sprzed rozszerzenia: brak klucza "dealers", znana oferta z Marek
    state = {"offers": {"1": {**_offer(1, 188).to_dict(), "station_id": None}}}
    offers = [_offer(1, 188), _offer(2, 187), _offer(3, 181), _offer(4, 186)]
    sent = _run(monkeypatch, state, offers)
    titles = [t for t, _, _ in sent]
    # nowa oferta z Żerania (salon obserwowany już wcześniej) -> zwykłe, wyróżnione powiadomienie
    assert any(t.startswith("⭐ ŻERAŃ · Nowy RAV4") for t in titles)
    # oferty z nowych salonów -> jedno zbiorcze powiadomienie
    assert sum("Nowy RAV4" in t for t in titles) == 1
    assert any("2 ofert z nowych" in t for t in titles)
    assert state["dealers"] == sorted(main.config.DEALERS)
    assert set(state["offers"]) == {"1", "2", "3", "4"}

    # kolejne uruchomienie: nowa oferta z nowego salonu już jest zgłaszana normalnie
    sent = _run(monkeypatch, state, offers + [_offer(5, 187)])
    assert [t for t, _, _ in sent] == ["Nowy RAV4: 150 000 zł"]


def test_zeran_price_drop_is_highlighted(monkeypatch):
    state = {"dealers": sorted(main.config.DEALERS),
             "offers": {"7": _offer(7, 186, 160_000).to_dict()}}
    sent = _run(monkeypatch, state, [_offer(7, 186, 150_000)])
    (title, msg, kw), = sent
    assert title.startswith("⭐ ŻERAŃ · Obniżka")
    assert kw["priority"] == 5 and "star" in kw["tags"]
    assert "ulubiony salon" in msg


def test_favorite_from_legacy_record():
    o = Offer("1", "Toyota Warszawa Żerań", "", 2023, 1, "Hybryda", 1, "", None)
    assert main.favorite(o) == "ŻERAŃ"
    assert main.favorite(_offer(2, 188)) is None
