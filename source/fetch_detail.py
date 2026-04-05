from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=chrome_options)

def parse_detail_from_soup(soup):
    data = {}

    # TÍTOL
    title = soup.select_one("h2.panel-title")
    data["title"] = title.get_text(strip=True) if title else None

    # ESTAT
    estat = soup.select_one("p.estat")
    data["status"] = estat.get_text(strip=True) if estat else None

    # PDFS
    pdfs = []
    for a in soup.select("td.icon a"):
        img = a.select_one("img[src*='icon-pdf']")
        if img:
            href = a.get("href")
            if href:
                pdfs.append(href)

    data["pdfs"] = pdfs

    # DETALLS
    details = {}
    for group in soup.select("dl.dades-oferta .dl-group"):
        dt = group.select_one("dt")
        dd = group.select_one("dd")
        if dt and dd:
            clau = dt.get_text(strip=True)
            valor = dd.get_text(" ", strip=True)
            details[clau] = valor

    data["details"] = details
    print(data)

    return data
def fetch_detail(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(0.5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    return parse_detail_from_soup(soup)
