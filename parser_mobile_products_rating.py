import requests
import variables
from bs4 import BeautifulSoup


PRODUCT_LINKS = variables.PRODUCT_LINKS


def open_page():
    with open("mobile_products.html", "r") as file:
        return file.read()


# def open_page(url):
#     try:
#         return requests.get(url)
#     except Exception:
#         return "Something wrong"


def parse_page(page):
    return BeautifulSoup(page, "lxml")


def find_product_rating(soup, tag_for_raging):
    return soup.find("table", {"id": "rating_overview_table"}).find(
        "p", string=tag_for_raging).find_parent("tr").find(
        "td", {"id": "product_rating_for_current_version"}).text.replace(" ", "")


def find_product_num_of_ratings(soup, tag_for_num_of_ratings):
    return soup.find("table", {"id": "rating_overview_table"}).find(
        "p", string=tag_for_num_of_ratings).find_parent("tr").find(
        "td", {"id": "product_ratings_count_for_current_version"}).text.replace(" ", "")


def main(platform, product_name, product_link):
    soup = parse_page(open_page())
    rating = float(find_product_rating(soup, product_name))
    num_of_ratings = int(find_product_num_of_ratings(soup, product_name))
    print(
        product_name, "for", platform, "has rating:", rating, "with number of votes", num_of_ratings
    )
    print(product_link)


if __name__ == '__main__':
    for key in PRODUCT_LINKS:
        product = list(PRODUCT_LINKS[key].items())
        main(key.split()[1], product[0][0], product[0][1])
