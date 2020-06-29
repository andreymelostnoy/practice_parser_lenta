import requests
import csv
import re
from bs4 import BeautifulSoup


def open_page():
    url = "https://lenta.ru"
    try:
        return requests.get(url)
    except Exception:
        print("Something wrong")


def find_html_elements(soup, class_, fresh=False):
    news_section = soup.find("section", {"class": class_})
    news_divs = news_section.find_all("div")
    links = []
    for div in news_divs:
        try:
            href = (div.find("a").get("href"))
            if href.startswith("/news") and href not in links:
                links.append(href)
        except:
            pass
    regex = r"\d\d:\d\d"
    elements = []
    for link in links:
        text = soup.find("a", {"href": link}).text
        name = re.sub(regex, "", text)
        elements.append({"name": name, "url": open_page().url.rstrip("/") + link})
    if fresh:
        first_element = soup.find("div", {"class": "first-item"}).find("h2").text
        first_element = re.sub(regex, "", first_element)
        elements[0]["name"] = first_element
    return elements


def find_news_fresh(soup):
    html_elements = find_html_elements(soup, "b-top7-for-main", fresh=True)
    return html_elements


def find_news_main(soup):
    html_elements = find_html_elements(soup, "b-yellow-box js-yellow-box")
    return html_elements


def write_output_to_file(news_fresh, news_main):
    def f(file_name, news):
        with open(file_name, "w", newline="") as file:
            columns = ["name", "url"]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(news)
    f("news_fresh.csv", news_fresh)
    f("news_main.csv", news_main)


def main():
    page = open_page().text
    soup = BeautifulSoup(page, "lxml")
    write_output_to_file(find_news_fresh(soup), find_news_main(soup))


if __name__ == '__main__':
    main()
