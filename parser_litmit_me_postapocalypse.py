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
    for book in list_of_books:
        name = book.find("span", {"itemprop": "name"})
        link = book.find("", {"": ""})
        author = book.find("", {"": ""})
        genre = book.find("", {"": ""})
        rating = book.find("", {"": ""})
        pages = book.find("", {"": ""})
        language = book.find("", {"": ""})
        year = book.find("", {"": ""})
        description = book.find("", {"": ""})


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
    print(len(list_of_books))
    # parsing_books(list_of_books)


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
