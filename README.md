

# <div align="center"> [DA-Python] Projet N°2 </div>
# <p align="center"><img width=40% src="https://github.com/hanroy/DevPy-P2/blob/main/img/webscrapping.png?raw=true"></p>
# <div align="center"> Script (ETL) d'extraction, transformation et de chargement de data depuis un site web </div>


## Table des matières
1. [Contexte du projet](#part1)
2. [Configuration de l'environnement](#part2)
3. [Contribution](#part3)

## <a name="part1"> 1. Contexte du projet: </a>

Extraire les données suivantes depuis le site https://books.toscrape.com/ puis les exporter un fichier csv:

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

## <a name="part2"> 2. Configuration de l'environnement: </a>

- Cloner ce repository 

```
git clone https://github.com/hanroy/DevPy-P2.git
```

- Se positionner dans le dossier 

```
cd DevPy-P2
```

- Créer un environnement via la commande 

```
virtualenv -p python3 venv
```

- Activer l'environnement:  

```
source venv/bin/activate
```

- Installer les dépendances

```
pip3 install -r requirements.txt
```

## <a name="part3"> 3. Contribution: </a>
Toute [contribution](https://github.com/hanroy/DevPy-P2/blob/main/CONTRIBUTING.md) est la bienvenue.
