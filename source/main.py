import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from fetch_list_selenium import fetch_all_titles_and_urls
from fetch_detail import parse_detail_from_soup


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    return webdriver.Chrome(options=chrome_options)


def scrape():
    print("Obtenint totes les oposicions del llistat...")
    entries = fetch_all_titles_and_urls()
    print(f"Total d'entrades trobades: {len(entries)}")

    driver = get_driver()
    dataset = []

    for i, entry in enumerate(entries, start=1):
        print(f"\n({i}/{len(entries)}) Processant: {entry['titol']}")
        url = entry["url"]

        try:
            driver.get(url)
            time.sleep(0.15)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            detail = parse_detail_from_soup(soup)

            row = {
                "titol": entry["titol"],
                "url": url,
                "estat": detail.get("estat"),
                **detail.get("detalls", {}),
                "pdfs": ", ".join(detail.get("pdfs", []))
            }

            dataset.append(row)
            print(f"Processat correctament")

        except Exception as e:
            print(f"Error processant {url}: {e}")

    driver.quit()
    print("\nScraping complet!")
    return dataset


if __name__ == "__main__":
    data = scrape()
    #TODO Generar dataset.
