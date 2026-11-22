# RAV4 watch

Powiadomienia na telefon o:

1. **nowych ofertach używanych Toyot RAV4** na [pewneauto.pl](https://pewneauto.pl/) w **22 salonach
   Toyota i Lexus w Warszawie i okolicach** (do ~35 km od centrum) – tylko hybrydy,
   rocznik **od 2023** (dodatkowo: o obniżce ceny już obserwowanej oferty). Powiadomienie zawiera:
   - **⭐ ŻERAŃ** w tytule i najwyższy priorytet dla ofert z salonu Żerań (znajomy mechanik),
   - wersję i napęd, kolor, tapicerkę, oznaczenia (bezwypadkowy, salon PL, FV 23%),
   - **porównanie z rynkiem** – medianę cen podobnych RAV4 (rocznik, przebieg, napęd) z całej Polski
     w programie Toyota Pewne Auto i różnicę w %,
   - dane do sprawdzenia auta na [historiapojazdu.gov.pl](https://historiapojazdu.gov.pl/)
     (nr rejestracyjny, VIN, data 1. rejestracji),
2. **promocji na nowego RAV4** – gdy cena bazowa „od …” na
   [toyota.pl/nowe-samochody/rav4](https://www.toyota.pl/nowe-samochody/rav4) spadnie poniżej **175 000 zł**.

3. **podsumowaniu tygodnia** (niedziela po 18:00) – wszystkie obserwowane oferty od najlepszej
   względem rynku, z liczbą dni na stronie, historią obniżek oraz listą aut, które zniknęły
   (sprzedane/zdjęte). Ręcznie: **Actions → RAV4 watch → Run workflow → „Wyślij teraz podsumowanie”**.

Skrypt uruchamia się co godzinę w GitHub Actions i zapisuje znane oferty w `state.json`.

## Konfiguracja (jednorazowo, ~5 minut)

1. Zainstaluj na telefonie darmową aplikację **ntfy** (Android: Google Play / F-Droid, iPhone: App Store).
2. W aplikacji „Subskrybuj temat” i wpisz trudną do zgadnięcia nazwę, np. `rav4-tomek-8f3k2q9x`
   (temat działa jak hasło – każdy, kto go zna, może czytać powiadomienia).
3. W repozytorium na GitHubie: **Settings → Secrets and variables → Actions → New repository secret**
   - nazwa: `NTFY_TOPIC`, wartość: ta sama nazwa tematu.
4. Upewnij się, że kod jest na domyślnej gałęzi (harmonogram działa tylko tam) i Actions są włączone
   (**Actions** → włącz workflow „RAV4 watch”).
5. Kliknij **Actions → RAV4 watch → Run workflow**. Pierwsze uruchomienie wyśle podsumowanie
   aktualnych ofert; kolejne – tylko nowości.

Opcjonalnie zamiast/obok ntfy: Telegram – sekrety `TELEGRAM_BOT_TOKEN` i `TELEGRAM_CHAT_ID`.

## Zmiana kryteriów

Wszystko w `carwatch/config.py`: salony (`DEALERS`, „station-id” z pewneauto.pl; ID i współrzędne salonów są w danych strony
[znajdz-dilera](https://pewneauto.pl/znajdz-dilera)), wyróżnione salony (`FAVORITE_DEALERS`), minimalny rocznik,
rodzaje napędu (domyślnie hybryda i hybryda plug-in), próg ceny nowego RAV4, powiadomienia o obniżkach,
dzień i godzina podsumowania tygodnia.

## Uruchomienie lokalne

```bash
pip install -r requirements.txt
NTFY_TOPIC=twoj-temat python -m carwatch.main
python -m pytest   # testy parserów
```

> Repozytorium wcześniej zawierało scraper Slowhop (nieaktualny) – dostępny w historii gita.
