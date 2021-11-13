from bs4 import BeautifulSoup   #un module qui permet de parser les pages html
import requests #module permettant d'utiliser le protocole http
from urllib.parse import urljoin #permet la gestion des url
import csv #permet la création et manipulation des fichiers csv
import os #permet d’effectuer des opérations courantes liées au système d’exploitation
import re #gère les expressions régulières
import sys #fournit des fonctions et des variables qui permettent d’interagir avec l’interpréteur Python

main_url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

response = requests.get(main_url)

if response.status_code != 200:
    print(f"UNREACHABLE URL response code {response.status_code}")
    sys.exit(1)
else:
    page = BeautifulSoup(response.content, "lxml")
    category = page.find('h1').get_text()

    urls = [main_url]
    pagination = page.select_one('li.current')

    if pagination is None:
        num_pages = 1

    else:
        page_indicator = page.find(class_='current').get_text().split()
        num_pages = int(page_indicator[3])

    for i in range(2, num_pages + 1):
        parts = "page-{}.html".format(i)
        links= urljoin(main_url, parts)
        urls.append(links)

directory_name = './data-{}'.format(category)
os.makedirs(directory_name, exist_ok = True)
img_directory = './images'
path = os.path.join(directory_name, img_directory)
os.makedirs(path, exist_ok = True)
csvname = 'data-{}.csv'.format(category)
filename = f"{directory_name}/{csvname}"

csvfile = open(filename, 'w')
csvwriter = csv.writer(csvfile)
fields = ["product_page_url","universal_product_code","title", "price_including_tax","price_excluding_tax","number_available","category","review_rating","image_url", "product_description"]
csvwriter.writerow(fields)

def create_csv (urls_1):
    for url in urls_1:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        books = soup.find("section")
        book_list = books.find_all(class_="product_pod")

        for book in book_list:
            # Get the product page url
            ref = book.find("a")["href"]
            book_url = urljoin(url, ref )
            response = requests.get(book_url)
            soup = BeautifulSoup(response.content, "lxml")

            universal_product_code = soup.find_all('tr')[0].get_text()
            title = soup.find('h1').get_text()
            price_including_tax = soup.find_all('td')[3].get_text()
            price_excluding_tax = soup.find_all('td')[2].get_text()
            number_available = soup.find_all('td')[5].get_text()
            product_description = soup.find_all('p')[3].get_text()
            category = soup.find_all('a')[3].get_text()
            review_rating = soup.find('p', class_='star-rating').get('class')[1]

            image_url = urljoin('https://books.toscrape.com/', soup.find("img")["src"] )
            csvwriter.writerow([book_url, universal_product_code.strip(), title.strip(), price_including_tax, price_excluding_tax, number_available, category, review_rating, image_url, product_description ])

            #Download images related books
            r = requests.get(image_url)
            # Create the folder in path.
            picture_name = re.sub('[^A-Za-z0-9]+', '', title)
            filename = os.path.join(path, picture_name)
            open(filename, 'wb').write(r.content)


create_csv(urls)
