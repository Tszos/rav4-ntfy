"""Ustawienia obserwatora ofert Toyoty RAV4."""

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    ),
    "Accept-Language": "pl-PL,pl;q=0.9",
}

TIMEZONE = "Europe/Warsaw"

# --- Samochody używane (platforma Toyota Pewne Auto, pewneauto.pl) --------
USED_BASE_URL = "https://pewneauto.pl"
USED_LISTING_PATH = "/oferty/brand/toyota/model/rav4"

# Salony Toyota/Lexus w Warszawie i okolicach (do ~35 km od centrum; następny
# jest Siedlce, 89 km). Klucz = "station-id" z filtra na pewneauto.pl, ID i
# współrzędne są w danych strony https://pewneauto.pl/znajdz-dilera.
DEALERS = {
    187: "Toyota Warszawa Czerniakowska",   # 3 km
    181: "Toyota Warszawa Wola",            # 4 km
    186: "Toyota Warszawa Żerań",           # 5 km
    13: "Lexus Warszawa Żerań",             # 5 km
    184: "Toyota Warszawa Bielany",         # 6 km
    180: "Toyota Warszawa Okęcie",          # 7 km
    204: "Toyota Warszawa Włochy",          # 7 km
    10: "Lexus Warszawa Wola",              # 7 km
    224: "Toyota Professional Bemowo",      # 8 km
    387: "Lexus Warszawa Bemowo",           # 8 km
    391: "Toyota Warszawa Bemowo",          # 9 km
    388: "Toyota Aleje",                    # 9 km
    315: "Toyota Wilanów",                  # 9 km
    188: "Toyota Warszawa Marki",           # 10 km
    179: "Toyota Warszawa Mościska Izabelin",  # 12 km
    20: "Lexus Warszawa Radość",            # 12 km
    189: "Toyota Warszawa Radość",          # 12 km
    15: "Lexus Warszawa Puławska",          # 14 km
    183: "Toyota Chodzeń Piaseczno",        # 14 km
    223: "Toyota Professional Wesoła",      # 16 km
    229: "Toyota Józefów",                  # 19 km
    380: "Toyota Mińsk Mazowiecki",         # 35 km
}

# Ulubione salony: oferty z nich są wyraźnie oznaczone (⭐ w tytule, najwyższy
# priorytet). Żerań – znajomy mechanik może sprawdzić auto na miejscu.
FAVORITE_DEALERS = {186: "ŻERAŃ", 13: "ŻERAŃ (Lexus)"}

MIN_YEAR = 2023
# Rodzaje napędu z karty oferty. Usuń "Hybryda Plug-in", jeśli interesują
# Cię wyłącznie zwykłe hybrydy.
ALLOWED_FUELS = {"Hybryda", "Hybryda Plug-in"}

# Powiadamiaj także o obniżce ceny już znanej oferty
NOTIFY_PRICE_DROPS = True

MAX_PAGES = 10  # zabezpieczenie przed nieskończoną paginacją

# --- Porównanie z rynkiem (wszystkie RAV4 w programie Toyota Pewne Auto) ---
MARKET_BASE_URL = "https://pewneauto.pl"
# wartości filtra "fuel" odpowiadające ALLOWED_FUELS
MARKET_FUEL_PARAMS = {"Hybryda": "hybrid", "Hybryda Plug-in": "hybrid-plug-in"}
MARKET_MAX_PAGES = 15
MIN_COMPARABLES = 4

# --- Cotygodniowe podsumowanie ---------------------------------------------
SUMMARY_WEEKDAY = 6  # 0 = poniedziałek ... 6 = niedziela
SUMMARY_HOUR = 18    # od tej godziny (czas polski) wysyłane jest podsumowanie

# --- Nowy RAV4 (toyota.pl) ------------------------------------------------
NEW_RAV4_URL = "https://www.toyota.pl/nowe-samochody/rav4"
NEW_PRICE_THRESHOLD = 175_000  # zł

# --- Błędy ---------------------------------------------------------------
# Run kończy się błędem (mail z GitHuba) dopiero, gdy to samo sprawdzenie pada tyle razy z rzędu.
FAIL_AFTER = 3

# --- Pliki ----------------------------------------------------------------
STATE_FILE = "state.json"
