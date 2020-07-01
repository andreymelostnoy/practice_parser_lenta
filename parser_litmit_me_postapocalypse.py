import requests
import csv
from datetime import datetime
import time
from bs4 import BeautifulSoup


def open_page(_url):
    try:
        return requests.get(_url)
    except Exception:
        print("Something wrong")


def find_list_of_books(soup):
    list_of_books = soup.find_all("table", {"class": "island"})
    return list_of_books


def parsing_books(list_of_books):
    global year, language, pages
    _books = []
    litmir = "https://www.litmir.me/"
    for book_ in list_of_books:
        book = book_.find("span", {"itemprop": "name"}).text
        try:
            link = litmir + book_.find("div", {"class": "book_name"}).find("a").get("href").lstrip("/")
        except:
            link = "Something wrong with " + book
        author = book_.find("span", {"itemprop": "author"}).find("a").text
        genre = book_.find("span", {"itemprop": "genre"}).text.replace("...", "")
        try:
            rating = book_.find("div", {"class": "description"}).find("span", {"class": "orange_desc"}).text
        except:
            rating = "Something wrong with " + book

        def find_pages_years_languages(element):
            return book_.find("span", string=element).find_parent("div").find_all("span", {"class": "desc2"})

        additional_elements = find_pages_years_languages("Язык книги:")
        if len(additional_elements) == 3:
            year = additional_elements[0].find("a").text.strip()
            language = additional_elements[1].text.strip()
            pages = additional_elements[2].text.strip()
        elif len(additional_elements) == 2:
            year = "Не указан"
            language = additional_elements[0].text.strip()
            pages = additional_elements[1].text.strip()
        description = book_.find("div", {"itemprop": "description"}).text
        _books.append({
            "book": book,
            "link": link,
            "author": author,
            "genre": genre,
            "rating": rating,
            "year": year,
            "language": language,
            "pages": pages,
            "description": description
        })
    return _books


def write_output_to_file(postapocalypse_books):
    def f(file_name, _books):
        with open(file_name, "a", newline="") as file:
            columns = ["book", "link", "author", "genre", "rating", "pages", "language", "year", "description"]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(_books)
    f("postapocalypse_books.csv", postapocalypse_books)


def main(_url):
    page = open_page(_url).text
    soup = BeautifulSoup(page, "lxml")
    list_of_books = find_list_of_books(soup)
    return parsing_books(list_of_books)


url = "https://www.litmir.me/bs?g=sg150&p={page}"

if __name__ == '__main__':
    start_time = datetime.now()
    books = []
    for i in range(1, 29):
        books.extend(main(url.format(page=i)))
    write_output_to_file(books)
    print(datetime.now() - start_time)
