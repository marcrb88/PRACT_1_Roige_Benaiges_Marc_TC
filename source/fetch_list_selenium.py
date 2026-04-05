from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

BASE_URL = "https://cido.diba.cat/oposicions?filtreParaulaClau%5Bkeyword%5D=&ordenacio=DEFAULT&ordre=DESC&showAs=GRID&filtreProximitat%5Bpoblacio%5D=&filtreProximitat%5Bkm%5D=&filtreProximitat%5Blatitud%5D=&filtreProximitat%5Blongitud%5D=&filtreDataPublicacio%5Bde%5D=&filtreDataPublicacio%5BfinsA%5D=&filtreEstat%5BterminiPendent%5D=1&filtreEstat%5BterminiObert%5D=1&filtreSeleccioTitulacio%5BtitulacioRequerida%5D%5Bkeyword%5D=&opcions-menu=&_token=TdBa8CZVfaNTC5TkdQ0vX63GKPRBmtuPgucxBmD2TDY&opcions-menu=&filtreMateria%5Boptions%5D%5B%5D=24"


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    return webdriver.Chrome(options=chrome_options)


def fetch_page(driver, page_number):
    url = f"{BASE_URL}&page={page_number}"
    driver.get(url)
    time.sleep(1.5)
    return BeautifulSoup(driver.page_source, "html.parser")


def extract_titles_from_soup(soup):
    items = soup.select("div.panel-oposicions")
    results = []

    for item in items:
        a = item.select_one("h2.panel-title a")
        if a:
            results.append({
                "title": a.get_text(strip=True),
                "url": "https://cido.diba.cat" + a.get("href")
            })

    return results


def fetch_all_titles_and_urls():
    driver = get_driver()

    all_results = []
    page = 1

    while True:
        print(f"Processant pàgina {page}...")

        soup = fetch_page(driver, page)
        entries = extract_titles_from_soup(soup)

        if not entries:
            print("No hi ha més pàgines.")
            break

        all_results.extend(entries)
        page += 1

    driver.quit()
    return all_results
