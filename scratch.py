import requests
from bs4 import BeautifulSoup


def fetch(address: str):
    _headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36"
    }
    _county_office_url = f"https://www.countyoffice.org/property-records-search/?q={address}"
    r = requests.get(_county_office_url, headers=_headers)
    r.raise_for_status()
    return r.content


def parse(page_data: str):
    soup = BeautifulSoup(page_data, features="html.parser")
    trs = soup.find_all("tr")
    for tr in trs:
        th_html = tr.find("th")
        th_raw = tr.find("th").text
        tds_html = tr.find("td")
        tds_raw = tds_html.text
        print(th_raw)
        print(tds_raw)



def address_data(address: str):
    _fetch = fetch(address)
    _parse = parse(_fetch)


address_data("501-elkhorn-pl-woodstock-ga-30189")
