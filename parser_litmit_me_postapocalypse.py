import requests
import csv
import re
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
    books = []
    litmir = "https://www.litmir.me/"
    for book in list_of_books:
        name = book.find("span", {"itemprop": "name"}).text
        link = litmir + book.find("div", {"class": "book_name"}).find("a").get("href").lstrip("/")
        author = book.find("span", {"itemprop": "author"}).find("a").text
        genre = book.find("span", {"itemprop": "genre"}).text.replace("...", "")
        rating = book.find("div", {"class": "description"}).find("span", {"class": "orange_desc"}).text
        pages = "test" # book.find("span", string="Год:")
        language = "test" # book.find("", {"": ""})
        year = "test" # book.find("", {"": ""})
        description = book.find("div", {"itemprop": "description"}).text
        books.append({
            "name": name,
            "link": link,
            "author": author,
            "genre": genre,
            "rating": rating,
            "pages": pages,
            "language": language,
            "year": year,
            "description": description
        })
    return books


def write_output_to_file(postapocalypse_books):
    def f(file_name, books):
        with open(file_name, "a", newline="") as file:
            columns = ["name", "link", "author", "genre", "rating", "pages", "language", "year", "description"]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(books)
    f("postapocalypse_books.csv", postapocalypse_books)


def main(_url):
    page = open_page(_url).text
    soup = BeautifulSoup(page, "lxml")
    list_of_books = find_list_of_books(soup)
    write_output_to_file(parsing_books(list_of_books))


url = "https://www.litmir.me/bs?g=sg150&p={page}"

if __name__ == '__main__':
    # books = []
    for i in range(1, 2):
        main(url.format(page=i))
        # books.append(main(url.format(page=i)))
    # books = [{"name": "1",
    #           "url": "2",
    #           "author": "3",
    #           "genre": "4",
    #           "rating": "5",
    #           "pages": "6",
    #           "language": "7",
    #           "year": "8",
    #           "description": "9"}]
    # write_output_to_file(books)
