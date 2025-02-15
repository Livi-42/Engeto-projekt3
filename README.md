# Engeto-projekt3
## Popis projektu
Tento Python skript slouží k extrahování volebních výsledků z webu www.volby.cz pro české volební okrsky a volební okrsky v zahraničí. Skript stahuje HTML stránku, extrahuje data o volebních výsledcích a ukládá je do CSV souboru pro další analýzu.<br/>

Skript obsahuje funkce pro zpracování výsledků jak z tuzemských volebních okrsků, tak i pro okrsky v zahraničí. Můžete specifikovat URL stránky a název výstupního CSV souboru jako argumenty při spuštění skriptu.<br/>

## Použití
1. Instalace závislostí:<br/> Před spuštěním skriptu je nutné nainstalovat potřebné knihovny:
```
pip install requests 
pip install beautifulsoup4
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

## Příklad výstupního CSV souboru<br/>
Výsledky budou uloženy do CSV souboru, kde každý řádek bude obsahovat následující sloupce:<br/>
- code: Kód okrsku
- location: Název obce
- registered: Počet registrovaných voličů
- envelopes: Počet odevzdaných obálek
- valid: Počet platných hlasů
- následují výsledky počtu hlasů pro jednotlivé politické strany

Nebo pro zahraniční volební okrsky:<br/>
- country: Kód státu
- city: Název města
- registered: Počet registrovaných voličů
- envelopes: Počet odevzdaných obálek
- valid: Počet platných hlasů
- následují výsledky počtu hlasů pro jednotlivé politické strany

## Poznámky<br/>
Tento skript je zaměřen na volební výsledky v roce 2017. Před použitím je nutné ověřit, zda stránka obsahuje požadované data pro zvolený rok.<br/>
Skript zpracovává volební okrsky jak v České republice, tak v zahraničí. Používá rozdílné metody pro získání dat v závislosti na lokalitě okrsku.<br/>
