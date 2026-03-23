from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

BASE_URL = "https://cido.diba.cat/oposicions?filtreEstat[terminiPendent]=1&filtreEstat[terminiObert]=1"

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
        titulo = item.select_one("h2.panel-title a")
        if titulo:
            results.append(titulo.get_text(strip=True))

    return results


def fetch_all_titles():
    driver = get_driver()

    all_results = []
    page = 1

    while True:
        print(f"Processant pàgina {page}...")

        soup = fetch_page(driver, page)
        titles = extract_titles_from_soup(soup)

        if not titles:
            print("No hi ha més pàgines.")
            break

        all_results.extend(titles)
        page += 1

    driver.quit()
    return all_results


if __name__ == "__main__":
    titles = fetch_all_titles()
    print(f"Total oposicions trobades: {len(titles)}")
    for t in titles:
        print(t)
