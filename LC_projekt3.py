"""
LC_projekt3.py: třetí projekt do Engeto Online Python Akademie

author: Livia Crhova
email: livia.crhova@gmail.com
"""
import sys
import requests
import csv
from bs4 import BeautifulSoup as bs
from bs4 import Tag

def save_data(data: list[dict[str,str]], file_name: str) -> None:
    """
    Tato funkce zapisuje seznam slovníků do CSV souboru, kde klíče slovníků 
    jsou názvy sloupců a hodnoty jsou odpovídající hodnoty v těchto sloupcích.

    Parametry:
    - data (list): Seznam slovníků, kde každý slovník obsahuje data pro jeden řádek tabulky. Klíče slovníků představují názvy sloupců a hodnoty jsou data pro tento sloupec.
    - file_name (str): Název souboru, do kterého budou data uložena.

    Výstup:
    - Při správných argumentech nevrací žádný výstup, ale zapisuje data do uvedeného csv souboru. 
    - Vrací řetězec "Dataset is empty" pokud je seznam 'data' prázdný
    - Pokud dojde k jiné chybě, vrací chybovou zprávu ve formátu "Error while trying to open the file and save the data: <chybová zpráva>".
    """    
    try:
        if len(data) == 0:
            return "Dataset is empty" 
    except Exception as e:   
        return f"Error while trying to open the file and save the data: {str(e)}"
    
    else:
        with open(file_name, mode="w", encoding="utf-8", newline='') as csv_file:
            columns = data[0].keys()
            zapis = csv.DictWriter(csv_file, fieldnames=columns)
            zapis.writeheader()
            zapis.writerows(data)


def get_html_soup(url: str) -> bs:
    """
    Tato funkce stáhne HTML stránku zadanou URL, ověří, zda byl požadavek úspěšný (status kód 200),
    a vrátí objekt BeautifulSoup pro analýzu HTML obsahu.

    Parametry:
    - url (str): URL adresa stránky k analýze.

    Výstup:
    - Vrací objekt BeautifulSoup pro analýzu HTML obsahu stránky.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error when loading the page: {response.status_code}")
        sys.exit()
    soup = bs(response.text, 'html.parser')
    return soup

def extract_summary_data_CZ(td_tag: list[Tag]) -> dict[str, str]:
    """
    Tato funkce extrahuje základní volební data o obci v ČR (registrovaní, obálky, platné hlasy).
    
    Parametry:
    - td_tag (list): Seznam HTML <td> tagů obsahujících volební data. Očekává se, 
                    že seznam bude mít minimálně 8 prvků, přičemž relevantní data 
                    jsou ve specifikovaných pozicích (indexy 3, 4 a 7).
    
    Výstup:
    - Vrací slovník s klíči 'registered', 'envelopes', 'valid' a jejich hodnotami.
    """
    registered = td_tag[3].get_text(strip=True)
    envelopes = td_tag[4].get_text(strip=True)
    valid = td_tag[7].get_text(strip=True)
    
    return {"registered": registered, "envelopes": envelopes, "valid": valid}

def extract_summary_data_abroad(td_tag: list[Tag]) -> dict[str, str]:
    """
    Tato funkce extrahuje základní volební data o zahraničním okrsku (registrovaní, obálky, platné hlasy).
    
    Parametry:
    - td_tag (list): Seznam HTML <td> tagů obsahujících volební data. Očekává se, 
                    že seznam bude mít minimálně 5 prvků, přičemž relevantní data 
                    jsou ve specifikovaných pozicích (indexy 0, 1 a 4).
    
    Výstup:
    - Vrací slovník s klíči 'registered', 'envelopes', 'valid' a jejich hodnotami.
    """
    registered = td_tag[0].get_text(strip=True)
    envelopes = td_tag[1].get_text(strip=True)
    valid = td_tag[4].get_text(strip=True)
    
    return {"registered": registered, "envelopes": envelopes, "valid": valid}



def extract_party_votes(td_tag: list[Tag]) -> dict[str, str]:
    """
    Extrahuje data o počtu hlasů pro jednotlivé politické strany z řádku volební tabulky ve volebním okrsku (v ČR nebo zahraničí).
    
    Parametry:
    - td_tag (list): Seznam <td> tagů, které obsahují data o politických stranách a jejich počtu hlasů.
                    Očekává se, že relevantní data jsou ve specifikovaných pozicích (indexy 1 a 2).
    
    Výstup:
    - Vrací slovník s názvem strany jako klíč a počtem hlasů jako hodnotu.
    """
    party = td_tag[1].get_text(strip=True)
    votes = td_tag[2].get_text(strip=True)
    
    return {party: votes}

def parse_tables(tables: list[bs], url: str) -> list[dict[str, str]]:
    """
    Prochází tabulkami s volebními výsledky jedného volebního okrsku (v ČR nebo zahraničí) a extrahuje relevantní data.
    
    Parametry:
    - tables (list): Seznam tabulek, které obsahují volební výsledky.
    - url (string): URL adresa stránky, která obsahuje volební výsledky pro konkrétní volební okrsek (v ČR nebo zahraničí).
                    URL je používána k rozlišení mezi volebním okrskem v ČR a zahraničním okrskem.
    
    Výstup:
    - Vrací seznam slovníků s volebními výsledky. První slovník obsahuje souhrnné údaje o volebním okrsku, následně jsou přidávány slovníky s údaji o politických stranách a počtu jejich hlasů.
    """
    votes_dictionary = []
    for table in tables:
        tr_tag_all = table.find_all("tr")                                   # V tabulkách identifikujeme "tr" tagy reprezentující oddělení jednotlivých řádků
        for tr in tr_tag_all:                                                              
            td_tag = tr.find_all("td")                                      # A následně v každém řádku hledáme "td" tagy reprezentujíci oddělení hodnot ve sloupcích každého řádku
            if len(td_tag) > 1:                                             # Hledáme řádek, který obsahuje více než 1 sloupec s hodnotami (to zn. není prázdný a není to hlavička)
                if len(votes_dictionary) == 0:                              # První tabulka obsahuje souhrnné údaje o volebním okrsku/obci. Takže pokud je slovník ještě prázdný, stojíme právě v první tabulce a můžeme extrahovat agregované data za volební okrsek
                    if url.startswith("https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=999997"):
                        summary_data = extract_summary_data_abroad(td_tag)  # ...za zahraniční volební okrsek
                    else:
                        summary_data = extract_summary_data_CZ(td_tag)      # ...nebo za volební okrsek v ČR
                    votes_dictionary.append(summary_data)
                else:                                                       # Následně, ostatní tabulky obsahují údaje o politických stranách a získaných hlasech, které doplníme do slovníku až za agregované data za volební okrsek
                    party_data = extract_party_votes(td_tag)
                    votes_dictionary.append(party_data)
    return votes_dictionary

def get_voting_data(url: str) -> dict[str, str]:
    """
    Funkce pro získání a zpracování volebních výsledků pro konkrétní volební okrsek (v ČR nebo zahraničí).
    Funkce stáhne HTML stránku zadanou URL, prozkoumá tabulky s výsledky voleb a vrátí strukturovaný slovník s výsledky.

    Parametry:
    - url (str): URL adresa stránky, která obsahuje volební výsledky pro konkrétní volební okrsek (v ČR nebo zahraničí).

    Výstup:
    - Vrací slovník (dict), který obsahuje volební výsledky, kde klíče jsou názvy položek (např. "registered", "envelopes", "valid")
      a hodnoty jsou příslušné výsledky voleb pro daný okrsek. V případě chyby při načítání stránky vrací prázdný slovník.
    """
    soup = get_html_soup(url)                                                       # Získání HTML
    tables = soup.find_all("table")                                                 # Najdeme všechny tabulky
    votes_dictionary = parse_tables(tables, url)                                    # Zpracujeme tabulky za volební okrsek a extrahujeme data
         
    final_dict = {key: value for d in votes_dictionary for key, value in d.items()} # Sloučení všech slovníků do jednoho
    return final_dict

def get_municipality_urls(soup: bs) -> list[str]:
    """
    Tato funkce získá všechny URL odkazy na volební okrsky z HTML stránky.

    Parametry:
    - soup: Objekt BeautifulSoup obsahující HTML stránku.

    Výstup:
    - Vrací seznam URL adres pro jednotlivé volební okrsky. Každý prvek seznamu je URL, která vede na podrobnosti volebního okrsku.
    """
    municipality_cells = soup.find_all("td", {"class": "cislo"})
    municipality_urls = [cell.find("a")["href"] for cell in municipality_cells]
    return municipality_urls

def extract_municipality_identification(tr_tag: bs, url: str) -> dict[str, str]:
    """
    Tato funkce extrahuje informace o kódu obce (code) a názvu obce (location) z řádku tabulky v případě volebního okrsku v ČR.
    Nebo název státu (country) a města (city) v případě zahraničního volebního okrsku.

    Parametry:
    - tr_tag (bs tag): Řádek tabulky (typicky <tr> tag), který obsahuje relevantní údaje pro volební okrsek.
    - url (str): Část url odkazu konkrétního volebního okrsku pro identifikaci, jestli sa jedná o ČR nebo zahraničí

    Výstup:
    - Vrací slovník obsahující identifikační informace o volebním okrsku:
        - pro obce v ČR klíče "code" pro kód obce a "location" pro název obce.
        - pro zahraničí klíče "country" pro název státu a "city" pro název města
    """
    td_tag = tr_tag.find_all("td")
    if url.startswith("ps311?xjazyk=CZ&xkraj=2&xobec=999997"):          #identifikace zahraničního volebního okrsku
        if len(td_tag) > 1:
            try:
                if int(td_tag[0].attrs["rowspan"]) > 10:
                    country = td_tag[1].get_text()
                    city = td_tag[2].get_text()
                elif int(td_tag[0].attrs["rowspan"]) > 1:     
                    country = td_tag[0].get_text()
                    city = td_tag[1].get_text()
                else:
                    country = td_tag[0].get_text()
                    city = td_tag[1].get_text()
            except KeyError:
                country = ""
                city = td_tag[0].get_text()
            return {"country": country, "city": city}
        return None
    
    else:                                                               #v ostatních případech, kdy se jedná o český volební okrsek
        if len(td_tag) > 1:
            code = td_tag[0].get_text()
            location = td_tag[1].get_text()
            return {"code": code, "location": location}
        return None


def process_table(soup: bs, tables: list[bs]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Tato funkce zpracuje tabulky na stránce a získá data o volebním okrsku (v ČR nebo zahraničí) a jeho výsledcích.
    Funkce pro každý volební okrsek extrahuje identifikační údaje (např. kód obce a název) a související volební výsledky (počet hlasů pro jednotlivé strany).

    Parametry:
    - soup: Objekt BeautifulSoup obsahující HTML stránku.
    - tables (list): Seznam tabulek, které obsahují data o volebních okrscích a jejich volebních výsledcích.

    Výstup:
    - Vrací tuple dvojice seznamů, kde první seznam obsahuje slovník dat o volebních okrscích (kód a název obce pro ČR
    nebo název státu a města pro zahraniční volební okrsek), a druhý seznam obsahuje výsledky voleb pro jednotlivé volební okrsky (počet hlasů pro jednotlivé politické strany).
    """
    data1, data2 = [], []
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    municipality_no = 0
    municipality_urls = get_municipality_urls(soup)

    for table in tables:
        tr_tag_all = table.find_all("tr")
        for tr in tr_tag_all:
            municipality_ID = extract_municipality_identification(tr, municipality_urls[0])
            if municipality_ID:                                                 # Zkontroluje, zda máme platný index v seznamu municipality_urls
                if municipality_no < len(municipality_urls):
                    municipality_url = municipality_urls[municipality_no]
                    data1.append(municipality_ID)
                    data2.append(get_voting_data(base_url + municipality_url))
                    municipality_no += 1         
    return data1, data2

def election_scraper() -> None:
    """
    Tato funkce slouží k extrahování dat o volbách z české webové stránky, kde jsou zveřejněny výsledky volebních okrsků z roku 2017.
    Funkce stáhne HTML stránku zadanou URL, zpracuje tabulky s informacemi o obcích a jejich výsledcích,
    a následně uloží tato data do CSV souboru.

    Parametry:
    - Funkce nevyžaduje žádné parametry. URL pro stažení a název výstupního souboru jsou získány z argumentů příkazové řádky (sys.argv).

    Výstup:
    - Funkce nevrací žádnou hodnotu. Data jsou uložena do souboru specifikovaného argumentem 'file' z příkazové řádky.
    - V případě chyby při stahování stránky, zpracování nebo ukládání dat bude vypsána chybová hláška. 
    """
    url = sys.argv[1]
    file = sys.argv[2]
    soup = get_html_soup(url)
    print(f"DOWNLOADING DATA FROM CHOSEN URL: {url}")

    tables = soup.find_all("table")                                 # Najdeme všechny tabulky na stránce

    data1, data2 = process_table(soup, tables)                      # Zpracujeme data z tabulek
    
    combined_data = [{**d1, **d2} for d1, d2 in zip(data1, data2)]  # Sloučíme data o okrscích a jejich výsledcích

    print(f"SAVING DATA TO THE FILE: {file}")                       
    save_data(combined_data, file)                                  # Uložíme data do souboru
    print(f"TERMINATING THE ELECTION-SCRAPER")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrect command, the script needs two arguments, one for the url address and one for the name of destination file in this form: python LC_projekt3.py <url> <file.csv>")
        sys.exit(1)
    else:
        election_scraper()
