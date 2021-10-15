from bs4 import BeautifulSoup 
import requests
from urllib.parse import urljoin

urls = ['http://books.toscrape.com/catalogue/category/books/mystery_3/index.html', 'https://books.toscrape.com/catalogue/category/books/mystery_3/page-2.html']



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

        
        print("Title of the book :" + soup.find('h1').get_text())
        print("price_including_tax: " + soup.find_all('tr')[3].get_text())
        print("price_excluding_tax: " + soup.find_all('tr')[2].get_text())     
        print("universal_ product_code (upc): " + soup.find_all('tr')[0].get_text())
        print("number_available: " + soup.find_all('tr')[5].get_text())
        print("product_description :" + soup.find_all('p')[3].get_text())
        print("category : " + soup.find_all('a')[3].get_text())
        print("review_rating :" + soup.find_all('tr')[6].get_text())
        image_url = soup.find_all('img')[0]
        print(image_url)
'''    
    # Get the books title
        title = book.select_one('a img')['alt']
        print ("Title of the book :" + title)
'''

        

