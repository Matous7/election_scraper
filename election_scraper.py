"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Matouš Kopáček
email: matouskopacek@gmail.com
discord: matousk_84638
"""

from bs4 import BeautifulSoup
from csv import writer
import requests
import sys


def ziskat_url(url):
    response = requests.get(url)
    web = response.text
    soup = BeautifulSoup(web, "html.parser")
    return soup

def ziskat_kody_mest(soup):
    city_codes = []
    td_codes = soup.find_all("td", class_="cislo")
    for code in td_codes:
        city_codes.append(code.text)
    return city_codes

def ziskat_nazvy_mest(soup):
    city_names = []
    td_names = soup.find_all("td", class_="overflow_name")
    for name in td_names:
        city_names.append(name.text)
    return city_names

def ziskat_odkazy(soup):
    LINKS = []
    td_links = soup.find_all("td", class_="cislo")
    for link in td_links:
        link = link.find("a")
        LINKS.append(link.get("href"))
    return LINKS

def scrapovat_info_a_ulozit(LINKS, city_codes, city_names, vystupni_soubor):
    with open(vystupni_soubor, mode="w", newline="", encoding="utf-8") as f:
        thewriter = writer(f)
        header = ["code", "location", "registered", "envelopes", "valid"]
        strany_header = [
            "Občanská demokratická strana", "Řád národa - Vlastenecká unie", "CESTA ODPOVĚDNÉ SPOLEČNOSTI",
            "Česká str.sociálně demokrat.", "Radostné Česko", "STAROSTOVÉ A NEZÁVISLÍ", "Komunistická str.Čech a Moravy",
            "Strana zelených", "ROZUMNÍ-stop migraci,diktát.EU", "Strana svobodných občanů",
            "Blok proti islam.-Obran.domova", "Občanská demokratická aliance", "Česká pirátská strana",
            "Referendum o Evropské unii", "TOP 09", "ANO 2011", "Dobrá volba 2016", "SPR-Republ.str.Čsl. M.Sládka",
            "Křesť.demokr.unie-Čs.str.lid.", "Česká strana národně sociální", "REALISTÉ", "SPORTOVCI",
            "Dělnic.str.sociální spravedl.", "Svob.a př.dem.-T.Okamura (SPD)", "Strana Práv Občanů"
        ]
        thewriter.writerow(header + strany_header)

        for index, link in enumerate(LINKS):
            links_url = "https://volby.cz/pls/ps2017nss/" + link
            response1 = requests.get(links_url)
            web1 = response1.text
            soup1 = BeautifulSoup(web1, "html.parser")

            CITY_CODES = city_codes[index]
            CITY_NAMES = city_names[index]
            VOLICI_V_SEZNAMU = soup1.find("td", class_="cislo", headers="sa2").text
            VYDANE_OBALKY = soup1.find("td", class_="cislo", headers="sa3").text
            PLATNE_HLASY = soup1.find("td", class_="cislo", headers="sa6").text

            strany = []

            headers_list = ["t1sa2 t1sb3", "t2sa2 t2sb3"]

            for headers in headers_list:
                td_votes_total = soup1.find_all("td", class_="cislo", headers=headers)
                strany.extend([vote.text for vote in td_votes_total])

            udaje = [CITY_CODES, CITY_NAMES, VOLICI_V_SEZNAMU, VYDANE_OBALKY, PLATNE_HLASY] + strany
            thewriter.writerow(udaje)

            print(f"Stahuji a zapisuji data. {index + 1} z {len(LINKS)} obcí.")

def scrapovat_a_ulozit(url, vystupni_soubor):
    soup = ziskat_url(url)
    # Získání kódů města
    city_codes = ziskat_kody_mest(soup)

    # Získání názvů měst
    city_names = ziskat_nazvy_mest(soup)

    # Získání odkazů
    LINKS = ziskat_odkazy(soup)

    # Scrapování detailů a uložení do souboru
    scrapovat_info_a_ulozit(LINKS, city_codes, city_names, vystupni_soubor)

if __name__ == "__main__":
    #Kontrola správného počtu argumentů
    if len(sys.argv) != 3:
        print("Pro správné spuštění programu zadejte: python election_scraper.py <odkaz> <vystupni_soubor>")
        sys.exit(1)

    #Přiřazení argumentů
    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]


    # Spuštění scraperu a zápisu do CSV
    scrapovat_a_ulozit(url, vystupni_soubor)
