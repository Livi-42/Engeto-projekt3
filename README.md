# Engeto-projekt3
## Popis projektu
Tento Python skript slouží k extrahování volebních výsledků z webu www.volby.cz pro české volební okrsky a volební okrsky v zahraničí. Skript stahuje HTML stránku, extrahuje data o volebních výsledcích a ukládá je do CSV souboru pro další analýzu.<br/>

Skript obsahuje funkce pro zpracování výsledků jak z tuzemských volebních okrsků, tak i pro okrsky v zahraničí. Můžete specifikovat URL stránky a název výstupního CSV souboru jako argumenty při spuštění skriptu.<br/>

## Použití
1. Instalace závislostí:<br/> Před spuštěním skriptu je nutné nainstalovat potřebné knihovny:
```
pip install requests beautifulsoup4
```

2. Spuštění skriptu:<br/> Skript se spouští z příkazového řádku. Použití je následující:
```
python LC_projekt3.py <url> <file.csv>
```
   
<br/>
url: URL stránka s volebními výsledky územního celku, kterou chcete zpracovat. URL stránka musí být uvedena v uvozovkách, např. "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"<br/>

file.csv: Název souboru, do kterého budou uložena extrahovaná data ve formátu CSV. Název souboru musí být uveden v uvozovkách, např. "soubor.csv"<br/>

3. Příklad použití:
```
python LC_projekt3.py "https://www.volby.cz/pls/ps2017nss/ps36?xjazyk=CZ" "output.csv"
```
   
Tento příkaz stáhne volební výsledky pro zahraniční okrsky a uloží je do souboru output.csv.

## Funkce
1. save_data(data: list, file_name: str) -> str<br/>
Funkce pro uložení seznamu slovníků do CSV souboru.<br/>

Parametry:<br/>
data (list): Seznam slovníků, kde každý slovník obsahuje data pro jeden řádek tabulky.<br/>
file_name (str): Název souboru, do kterého budou data uložena.<br/>

Výstup:<br/>
Pokud je seznam data prázdný, vrací "Dataset is empty".<br/>
Pokud dojde k chybě při zápisu do souboru, vrací chybovou zprávu.<br/>

2. get_municipality_data(url: str) -> dict<br/>
Funkce pro extrahování volebních výsledků pro tuzemské volební okrsky.<br/>

Parametry:<br/>
url (str): URL adresa stránky s výsledky voleb pro konkrétní okrsek.<br/>

Výstup:<br/>
Vrací slovník s volebními výsledky (např. registrovaní voliči, obálky, platné hlasy).<br/>

3. get_municipality_data_abroad(url: str) -> dict<br/>
Funkce pro extrahování volebních výsledků pro volební okrsky v zahraničí.<br/>

Parametry:<br/>
url (str): URL adresa stránky s výsledky voleb pro konkrétní okrsek v zahraničí.<br/>

Výstup:<br/>
Vrací slovník s volebními výsledky (např. registrovaní voliči, obálky, platné hlasy).<br/>

4. election_scraper_CZ(url: str, file: str)<br/>
Funkce pro extrahování dat o volbách pro tuzemské okrsky a jejich uložení do CSV souboru.<br/>

Parametry:<br/>
url (str): URL stránka s výsledky voleb.<br/>
file (str): Název výstupního souboru.<br/>

5.election_scraper_abroad(url: str, file: str)<br/>
Funkce pro extrahování dat o volbách pro okrsky v zahraničí a jejich uložení do CSV souboru.<br/>

Parametry:<br/>
url (str): URL stránka s výsledky voleb v zahraničí.<br/>
file (str): Název výstupního souboru.<br/>



## Příklad výstupního CSV souboru<br/>
Výsledky budou uloženy do CSV souboru, kde každý řádek bude obsahovat následující sloupce:<br/>
- code: Kód okrsku
- location: Název obce
- registered: Počet registrovaných voličů
- envelopes: Počet odevzdaných obálek
- valid: Počet platných hlasů
- následují výsledky počtu hlasů pro jednotlivé politické strany

## Poznámky<br/>
Tento skript je zaměřen na volební výsledky v roce 2017. Před použitím je nutné ověřit, zda stránka obsahuje požadované data pro zvolený rok.<br/>
Skript zpracovává volební okrsky jak v České republice, tak v zahraničí. Používá rozdílné metody pro získání dat v závislosti na lokalitě okrsku.<br/>
