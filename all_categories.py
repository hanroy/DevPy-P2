from bs4 import BeautifulSoup   #un module qui permet de parser les pages html
import requests #module permettant d'utiliser le protocole http
from urllib.parse import urljoin #permet la gestion des url
import csv #permet la création et manipulation des fichiers csv
import os #permet d’effectuer des opérations courantes liées au système d’exploitation
import re #gère les expressions régulières

############################-- Declaration des functions --#############################


def get_categories():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    sidebar = soup.find("ul", class_="nav nav-list").find_all("a")
    categories = []
    for cate in sidebar:
        categories_name = (cate.text.strip()) # extraire les noms des catégories dans la sidebar
        categories_url = (url + cate.get("href").strip()) # extraire l'url de chaque catégorie
        categories.append((categories_name, categories_url)) 
   
    return categories
    

def get_all_category_urls(category_link): # traitement de la pagination
    all_book_urls = []
    for u in category_link:
        response = requests.get(u)
        page = BeautifulSoup(response.content, "lxml")

        pagination = page.select_one('li.current')
        
        if pagination is None:
            num_pages = 1
        else:
            page_indicator = page.find(class_='current').get_text().split()
            num_pages = int(page_indicator[3])
        
        all_book_urls.append(u) #un premier traitement pour toutes les catégories sans pagination

        for i in range(2, num_pages + 1):
            parts = "page-{}.html".format(i)
            linkss = urljoin(u, parts)
            all_book_urls.append(linkss) # ajout des urls des catégories avec pagination

    return all_book_urls


############################-- Traitement des fonctions --#############################

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")


list_of_categories = get_categories()

for index in list_of_categories[1:]: #traitement des catégories sans prise en compte de la caté Books
    links = []
    category_name = index[0]
    category_link = index[1]
    links.append(category_link)  

# créer le dossier data + les csv qui porteront la data de chaque catégorie/livre
    csvfolder = './books_data'
    os.makedirs("books_data", exist_ok=True)
    csvpath = f"{csvfolder}/{'data-{}.csv'.format(category_name)}" 
    csvname = open(csvpath, "w")           
    csvwriter = csv.writer(csvname)
    fields = ["product_page_url","universal_product_code","title", "price_including_tax","price_excluding_tax","number_available","category","review_rating","image_url", "product_description"]
    csvwriter.writerow(fields)

    # print les urls des catégories et les paginations respectives
    all_categories_url = get_all_category_urls(links)

    for book_urls in all_categories_url:
        response = requests.get(book_urls)
        soup = BeautifulSoup(response.content, "lxml")
        books = soup.find("section")
        book_list = books.find_all(class_="product_pod")

        # extraire l'url de chaque livre
        for book in book_list:
            ref = book.find("a")["href"]
            book_url = urljoin(book_urls, ref)
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
            print(category_name + "---> " + title)
            csvwriter.writerow([book_url, universal_product_code.strip(), title.strip(), price_including_tax, price_excluding_tax, number_available, category, review_rating, image_url, product_description ])


            # Download covers pictures
            os.makedirs('covers', exist_ok = True)
            r = requests.get(image_url)
            picture_name = re.sub('[^A-Za-z0-9]+', '', title)
            filename = os.path.join('covers', picture_name)
            open(filename, 'wb').write(r.content)

