from bs4 import BeautifulSoup                                                               # Pour le scraping HTML
import requests                                                                             # Pour faire des requêtes HTTP
import pandas as pd                                                                         # Pour la manipulation des données
import numpy as np                                                                          # Pour les opérations numériques
import matplotlib.pyplot as plt                                                             # Pour la visualisation des données

# Fonction de scrapping des tirages loto
def scrap_loto_numbers():
    """
    Fonction pour extraire les tirages du loto depuis un site web.
    """
    my_list=[]

    # URL du site de l'histoire des tirages
    loto_url = "http://loto.akroweb.fr/loto-historique-tirages/"

    # Récupération de la page et parsing
    page = requests.get(loto_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Récupération du tableau des tirages (composant table de la page)
    body = soup.find('table')

    # Récupération des lignes du tableau (composants tr de la page)
    tirage_line = body.find_all('tr')

    # Récupération des valeurs des tirages
    for value in tirage_line:
        # Notre dictionnaire sera composé de plusieurs colonnes :
        # - day : jour de la semaine du tirage
        # - month_year : jour, mois et année du tirage
        # - num0 à num4 : les 5 numéros tirés
        # - chance : le numéro chance
        my_dict = {}

        # Création d'un tableau avec pour élément les valeurs des tirages
        res = value.text.split('\n')

        my_dict['day'] = res[2]         # Jour de la semaine du tirage
        my_dict['month_year']=res[3]    # Jour, mois et année du tirage

        # Récupération des numéros et ajout dans le dictionnaire
        for i,val in enumerate(res[5:10]):
            my_dict['num'+str(i)]=int(val)

        # Récupération du numéro chance
        my_dict['chance']=int(res[10])

        # Ajout du dictionnaire à la liste
        my_list.append(my_dict)

    # Création du dataframe
    return pd.DataFrame(my_list)

# Calcul de la fréquence de tirage de chaque numéro
def calculate_frequencies(df):
    freqs = []
    for val in range(50):                                    # Itération pour chaque numéro possible (de 1 à 50)
        count = ((df['num0'] == val+1).sum() +               # Comptage du nombre d'occurrences de chaque numéro dans les tirages
                 (df['num1'] == val+1).sum() +
                 (df['num2'] == val+1).sum() +
                 (df['num3'] == val+1).sum() +
                 (df['num4'] == val+1).sum())
        freqs.append(count)                                   # Ajout du nombre d'occurrences à la liste des fréquences

    ax = plt.gca()                                           # Récupération de l'axe actuel
    ax.invert_yaxis()                                        # Inversion de l'axe y pour afficher les numéros dans l'ordre décroissant
    plt.gcf().set_size_inches(5, 4)                          # Définition de la taille de la figure
    heatmap = plt.pcolor(np.reshape(np.array(freqs), (5, 10)), cmap=plt.cm.Blues)  # Création d'un heatmap avec les fréquences
