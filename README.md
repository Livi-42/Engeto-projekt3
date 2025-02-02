# Engeto-projekt3
## Popis projektu
Tento Python skript slouží k extrahování volebních výsledků z webu www.volby.cz pro české volební okrsky a volební okrsky v zahraničí. Skript stahuje HTML stránku, extrahuje data o volebních výsledcích a ukládá je do CSV souboru pro další analýzu.<br/>

Skript obsahuje funkce pro zpracování výsledků jak z tuzemských volebních okrsků, tak i pro okrsky v zahraničí. Můžete specifikovat URL stránky a název výstupního CSV souboru jako argumenty při spuštění skriptu.<br/>

## Použití
1. Instalace závislostí: Před spuštěním skriptu je nutné nainstalovat potřebné knihovny:
```
pip install requests beautifulsoup4
```

3. Spuštění skriptu: Skript se spouští z příkazového řádku. Použití je následující:
```
python LC_projekt3.py <url> <file.csv>
```
   

<url>: URL stránka s volebními výsledky územního celku, kterou chcete zpracovat. URL stránka musí být uvedena v uvozovkách, např. "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"<br/>

<file.csv>: Název souboru, do kterého budou uložena extrahovaná data ve formátu CSV. Název souboru musí být uveden v uvozovkách, např. "soubor.csv"<br/>

3. Příklad použití:
```
python LC_projekt3.py "https://www.volby.cz/pls/ps2017nss/ps36?xjazyk=CZ" "output.csv"
```
   
Tento příkaz stáhne volební výsledky pro zahraniční okrsky a uloží je do souboru output.csv.

## Funkce
1. save_data(data: list, file_name: str) -> str
Funkce pro uložení seznamu slovníků do CSV souboru.

Parametry:
data (list): Seznam slovníků, kde každý slovník obsahuje data pro jeden řádek tabulky.
file_name (str): Název souboru, do kterého budou data uložena.

Výstup:
Pokud je seznam data prázdný, vrací "Dataset is empty".
Pokud dojde k chybě při zápisu do souboru, vrací chybovou zprávu.

2. get_municipality_data(url: str) -> dict
Funkce pro extrahování volebních výsledků pro tuzemské volební okrsky.

Parametry:
url (str): URL adresa stránky s výsledky voleb pro konkrétní okrsek.

Výstup:
Vrací slovník s volebními výsledky (např. registrovaní voliči, obálky, platné hlasy).

3. get_municipality_data_abroad(url: str) -> dict
Funkce pro extrahování volebních výsledků pro volební okrsky v zahraničí.

Parametry:
url (str): URL adresa stránky s výsledky voleb pro konkrétní okrsek v zahraničí.

Výstup:
Vrací slovník s volebními výsledky (např. registrovaní voliči, obálky, platné hlasy).

4. election_scraper_CZ(url: str, file: str)
Funkce pro extrahování dat o volbách pro tuzemské okrsky a jejich uložení do CSV souboru.

Parametry:
url (str): URL stránka s výsledky voleb.
file (str): Název výstupního souboru.

5.election_scraper_abroad(url: str, file: str)
Funkce pro extrahování dat o volbách pro okrsky v zahraničí a jejich uložení do CSV souboru.

Parametry:
url (str): URL stránka s výsledky voleb v zahraničí.
file (str): Název výstupního souboru.



## Příklad výstupního CSV souboru
Výsledky budou uloženy do CSV souboru, kde každý řádek bude obsahovat následující sloupce:
- code: Kód okrsku
- location: Název obce
- registered: Počet registrovaných voličů
- envelopes: Počet odevzdaných obálek
- valid: Počet platných hlasů
- následují výsledky počtu hlasů pro jednotlivé politické strany

## Poznámky
Tento skript je zaměřen na volební výsledky v roce 2017. Před použitím je nutné ověřit, zda stránka obsahuje požadované data pro zvolený rok.
Skript zpracovává volební okrsky jak v České republice, tak v zahraničí. Používá rozdílné metody pro získání dat v závislosti na lokalitě okrsku.
