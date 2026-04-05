from pathlib import Path
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from export_dataset import save_dataset_as_csv
from fetch_list_selenium import fetch_all_titles_and_urls
from fetch_detail import parse_detail_from_soup


DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "dataset" / "cido_oposicions.csv"


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
        print(f"\n({i}/{len(entries)}) Processant: {entry['title']}")
        url = entry["url"]

        try:
            driver.get(url)
            time.sleep(0.15)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            detail = parse_detail_from_soup(soup)

            row = {
                "title": entry["title"],
                "url": url,
                "status": detail["status"],
                **detail["details"],
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
    output_path = save_dataset_as_csv(data, DEFAULT_OUTPUT_PATH)
    print(f"\nDataset guardat a: {output_path}")
