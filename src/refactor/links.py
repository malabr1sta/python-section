import datetime
from datetime import date

from bs4 import BeautifulSoup


def parse_page_links(html: str, start_date: date, end_date: date, url: str):
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href = href.split("?")[0]
        if "/upload/reports/oil_xls/oil_xls_" not in href or not href.endswith(".xls"):
            continue

        try:
            date = href.split("oil_xls_")[1][:8]
            file = datetime.datetime.strptime(date, "%Y%m%d").date()
            if start_date <= file <= end_date:
                u = href if href.startswith("http") else f"https://spimex.com{href}"
                results.append((u, file))
            else:
                print(f"Ссылка {href} вне диапазона дат")
        except Exception as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results
