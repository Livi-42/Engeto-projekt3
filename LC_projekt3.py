"""
LC_projekt3.py: třetí projekt do Engeto Online Python Akademie

author: Livia Crhova
email: livia.crhova@gmail.com
"""
import sys
import requests
import csv
from bs4 import BeautifulSoup as bs

base_url = "https://www.volby.cz/pls/ps2017nss/"
final_list = []

def save_data(data:list, file_name: str) -> str:
    """
    Tato funkce zapisuje seznam slovníků do CSV souboru, kde klíče slovníků 
    jsou názvy sloupců a hodnoty jsou odpovídající hodnoty v těchto sloupcích.

    Parametry:
    - data (list): Seznam slovníků, kde každý slovník obsahuje data pro jeden řádek tabulky. Klíče slovníků představují názvy sloupců a hodnoty jsou data pro tento sloupec.
    - file_name (str): Název souboru, do kterého budou data uložena.

    Výstup:
    - Vrací řetězec:
      - `"Dataset is empty"` pokud je seznam `data` prázdný.
      - Pokud dojde k chybě při zapisování, vrací chybovou zprávu ve formátu `"Error: <chybová zpráva>"`.
    """
    try:
        with open(file_name, mode="w", encoding="utf-8", newline='') as csv_file:
            if not data:
                return "Dataset is empty"
            columns = data[0].keys()
            zapis = csv.DictWriter(csv_file, fieldnames=columns)
            zapis.writeheader()
            zapis.writerows(data)
    except Exception as e:
        return f"Error: {str(e)}"



def get_municipality_data(url):
    """
    Tato funkce slouží k extrahování volebních výsledků pro konkrétní volební okrsek v ČR.
    Funkce stáhne HTML stránku zadanou URL, prozkoumá tabulky s výsledky voleb a vrátí strukturovaný slovník s výsledky.

    Parametry:
    - url (str): URL adresa stránky, která obsahuje volební výsledky pro konkrétní volební okrsek v zahraničí.

    Výstup:
    - Vrací slovník (dict), který obsahuje volební výsledky, kde klíče jsou názvy položek (např. "registered", "envelopes", "valid")
      a hodnoty jsou příslušné výsledky voleb pro daný okrsek. V případě chyby při načítání stránky vrací prázdný seznam.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error when loading the page: {response.status_code}")
        return[]
    soup = bs(response.text, 'html.parser')
    tables = soup.find_all("table")
    votes_dictionary = []
    
    for table in tables:
        tr_tag_all = table.find_all("tr")
        for tr in tr_tag_all[2:]:
            td_tag = tr.find_all("td")
            if len(td_tag) > 1: 
                if len(votes_dictionary) == 0:
                    registered = td_tag[3].get_text(strip=True)
                    envelopes = td_tag[4].get_text(strip=True)
                    valid = td_tag[7].get_text(strip=True)
                    votes_dictionary.append({"registered": registered})
                    votes_dictionary.append({"envelopes": envelopes})
                    votes_dictionary.append({"valid": valid})
                else:
                    party = td_tag[1].get_text(strip=True)
                    votes = td_tag[2].get_text(strip=True)
                    votes_dictionary.append({party: votes})
    final_dict = {key: value for d in votes_dictionary for key, value in d.items()}
    return final_dict

def get_municipality_data_abroad(url):
    """
    Tato funkce slouží k extrahování volebních výsledků pro konkrétní volební okrsek v zahraničí.
    Funkce stáhne HTML stránku zadanou URL, prozkoumá tabulky s výsledky voleb a vrátí strukturovaný slovník s výsledky.

    Parametry:
    - url (str): URL adresa stránky, která obsahuje volební výsledky pro konkrétní volební okrsek v zahraničí.

    Výstup:
    - Vrací slovník (dict), který obsahuje volební výsledky, kde klíče jsou názvy položek (např. "registered", "envelopes", "valid")
      a hodnoty jsou příslušné výsledky voleb pro daný okrsek. V případě chyby při načítání stránky vrací prázdný seznam. 
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error when loading the page: {response.status_code}")
        return[]
    soup = bs(response.text, 'html.parser')
    tables = soup.find_all("table")
    votes_dictionary = []
    
    for table in tables:
        tr_tag_all = table.find_all("tr")
        for tr in tr_tag_all[1:]:
            td_tag = tr.find_all("td")
            if len(td_tag) > 1: 
                if len(votes_dictionary) == 0:
                    registered = td_tag[0].get_text(strip=True)
                    envelopes = td_tag[1].get_text(strip=True)
                    valid = td_tag[4].get_text(strip=True)
                    votes_dictionary.append({"registered": registered})
                    votes_dictionary.append({"envelopes": envelopes})
                    votes_dictionary.append({"valid": valid})
                else:
                    party = td_tag[1].get_text(strip=True)
                    votes = td_tag[2].get_text(strip=True)
                    votes_dictionary.append({party: votes})
    final_dict = {key: value for d in votes_dictionary for key, value in d.items()}
    return final_dict

def election_scraper_CZ(url, file):
    """
    Tato funkce slouží k extrahování dat o volbách z české webové stránky, kde jsou zveřejněny výsledky volebních okrsků.
    Funkce stáhne HTML stránku zadanou URL, zpracuje tabulky s informacemi o obcích a jejich výsledcích,
    a následně uloží tato data do CSV souboru.

    Parametry:
    - url (str): URL adresa stránky, která obsahuje tabulky s volebními výsledky.
    - file (str): Název souboru, do kterého budou uložena extrahovaná data ve formátu CSV.

    Výstup:
    - Funkce nevrací žádnou hodnotu. Data jsou uložena do souboru specifikovaného v parametru `file`.
    - V případě chyby při stahování stránky nebo zpracování dat bude vypsána chybová hláška. 
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error when loading the page: {response.status_code}")
        return
    else:
        print(f"DOWNLOADING DATA FROM CHOSEN URL: {url}")
    soup = bs(response.text, 'html.parser')
    tables = soup.find_all("table")
    data1, data2 = [], []
    municipality_no = 0
    for table in tables:
        tr_tag_all = table.find_all("tr")
        for tr in tr_tag_all:
            td_tag = tr.find_all("td")
            if len(td_tag) > 1:
                municipality_cells = soup.find_all("td", {"class": "cislo"} )
                if municipality_no < len(municipality_cells):
                    municipality_url = municipality_cells[municipality_no].find("a")["href"]
                    data1.append({
                        "code":td_tag[0].get_text(),
                        "location": td_tag[1].get_text()
                    })
                    data2.append(get_municipality_data(base_url+municipality_url))
                    municipality_no += 1
    combined_data = [{**d1, **d2} for d1, d2 in zip(data1, data2)]
    print(f"SAVING DATA TO THE FILE: {file}")
    save_data(combined_data, file)
    print(f"TERMINATING THE ELECTION-SCRAPER")

def election_scraper_abroad(url, file):
    """
    Tato funkce slouží k extrahování dat o volbách z české webové stránky, kde jsou zveřejněny výsledky volebních okrsků v zahraničí.
    Funkce stáhne HTML stránku zadanou URL, zpracuje tabulky s informacemi o obcích a jejich výsledcích,
    a následně uloží tato data do CSV souboru.

    Parametry:
    - url (str): URL adresa stránky, která obsahuje tabulky s volebními výsledky.
    - file (str): Název souboru, do kterého budou uložena extrahovaná data ve formátu CSV.

    Výstup:
    - Funkce nevrací žádnou hodnotu. Data jsou uložena do souboru specifikovaného v parametru `file`.
    - V případě chyby při stahování stránky nebo zpracování dat bude vypsána chybová hláška.  
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error when loading the page: {response.status_code}")
        return
    else:
        print(f"DOWNLOADING DATA FROM CHOSEN URL: {url}")
    soup = bs(response.text, 'html.parser')
    tables = soup.find_all("table")
    data1, data2 = [], []
    municipality_no = 0
    for table in tables:
        tr_tag_all = table.find_all("tr")
        for tr in tr_tag_all:
            td_tag = tr.find_all("td")
            if len(td_tag) > 1:
                municipality_cells = soup.find_all("td", {"class": "cislo"} )
                if municipality_no < len(municipality_cells):
                    municipality_url = municipality_cells[municipality_no].find("a")["href"]
                    try:
                        if int(td_tag[0].attrs["rowspan"]) > 10:
                            data1.append({
                            "country":td_tag[1].get_text(),
                            "city": td_tag[2].get_text()
                            })
                        elif int(td_tag[0].attrs["rowspan"]) > 1:     
                            data1.append({
                            "country":td_tag[0].get_text(),
                            "city": td_tag[1].get_text()
                            })
                        else:
                            data1.append({
                            "country": td_tag[0].get_text(),
                            "city": td_tag[1].get_text()
                            })
                    except KeyError:
                        data1.append({
                        "country": "",
                        "city": td_tag[0].get_text()
                        })
                    data2.append(get_municipality_data_abroad(base_url+municipality_url))
                    municipality_no += 1
    combined_data = [{**d1, **d2} for d1, d2 in zip(data1, data2)]
    print(f"SAVING DATA TO THE FILE: {file}")
    save_data(combined_data, file)
    print(f"TERMINATING THE ELECTION-SCRAPER")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Instructions for the command: python LC_projekt3.py <url> <file.csv>")
        sys.exit(1)
    else:
        url = sys.argv[1]
        file = sys.argv[2]
        if url == "https://www.volby.cz/pls/ps2017nss/ps36?xjazyk=CZ":
            election_scraper_abroad(url, file)
        else:
            election_scraper_CZ(url, file)
