import datetime
from datetime import date

import requests
from bs4 import BeautifulSoup


XLS_LINK_CLASS = "accordeon-inner__item-title link xls"


def get_html(url: str, timeout: int = 10) -> str:
    """
    Загружает HTML-код страницы по указанному URL.
    """
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def process_bulletin_link(
    href: str,
    start_date: datetime.date,
    end_date: datetime.date,
    base_url: str = "https://spimex.com"
) -> tuple[str, date] | None:
    """
    Обрабатывает одну ссылку на бюллетень.
    """
    if not href:
        return None

    base_href = href.split("?")[0]
    if (
        "/upload/reports/oil_xls/oil_xls_" not in base_href
        or not base_href.endswith(".xls")
    ):
        return None

    try:
        date_str = base_href.split("oil_xls_")[1][:8]
        bulletin_date = datetime.datetime.strptime(
            date_str, "%Y%m%d"
        ).date()
        if start_date <= bulletin_date <= end_date:
            absolute_url = (
                base_href if base_href.startswith("http")
                else f"{base_url}{base_href}"
            )
            return (absolute_url, bulletin_date)
        else:
            print(f"Ссылка {base_href} вне диапазона дат")
    except Exception as error:
        print(f"Не удалось извлечь дату из ссылки {base_href}: {error}")
    return None


def parser_bulletin_links(
    url: str, start_date: date, end_date: date
) -> list[tuple[str, date]]:
    """
    Парсит ссылки на бюллетени с одной страницы.

    :param url: базовый URL страницы
    :param start_date: начальная дата
    :param end_date: конечная дата
    :return: список кортежей (ссылка, дата)
    """
    results = []
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_=XLS_LINK_CLASS)

    for link in links:
        href = link.get("href")
        processed = process_bulletin_link(
            href, start_date, end_date
        )
        if processed is not None:
            results.append(processed)

    return results
