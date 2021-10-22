from bs4 import BeautifulSoup 
import requests
from urllib.parse import urljoin

urls = ['http://books.toscrape.com/catalogue/category/books/mystery_3/index.html', 'https://books.toscrape.com/catalogue/category/books/mystery_3/page-2.html']

# open a file in append mode to write into in the same directory where we ran this script from
csvfile = open('data.csv', 'w')
csvwriter = csv.writer(csvfile)
fields = ["product_page_url","universal_product_code","title", "price_including_tax","price_excluding_tax","number_available","category","review_rating","image_url", "product_description"]
csvwriter.writerow(fields)


for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    books = soup.find("section")
    book_list = books.find_all(class_="product_pod")
 
    for book in book_list:
        # Get the product page url
        ref = book.find("a")["href"]
        book_url = urljoin(url, ref )
        #print ("URL of the book :" + book_url)
        response = requests.get(book_url)
        soup = BeautifulSoup(response.content, "lxml")


        universal_product_code = soup.find_all('tr')[0].get_text() 
        title = soup.find('h1').get_text() 
        price_including_tax = soup.find_all('td')[3].get_text()
        price_excluding_tax = soup.find_all('td')[2].get_text()
        number_available = soup.find_all('td')[5].get_text() 
        product_description = soup.find_all('p')[3].get_text()
        category = soup.find_all('a')[3].get_text() 
        review_rating = soup.find_all('td')[6].get_text() 
        image_url = urljoin('https://books.toscrape.com/', soup.find("img")["src"] ) 
        csvwriter.writerow([book_url, universal_product_code.strip(), title.strip(), price_including_tax, price_excluding_tax, number_available, category, review_rating, image_url, product_description ]
