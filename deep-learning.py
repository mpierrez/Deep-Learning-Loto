import numpy as np                                       # Importation de la bibliothèque NumPy pour les opérations numériques
import matplotlib.pyplot as plt                          # Importation de la bibliothèque Matplotlib pour la visualisation des données
import pickle                                            # Importation de la bibliothèque pickle pour la sérialisation des données
from sklearn.preprocessing import StandardScaler         # Importation de la fonction StandardScaler de scikit-learn pour la mise à l'échelle des données
from keras.callbacks import EarlyStopping                # Importation de la classe EarlyStopping de Keras pour arrêter l'entraînement du modèle si nécessaire
from loto_functions import *                             # Importation de la fonction de scrapping des tirages loto
from utils import *                                      # Importation de fonctions utilitaires
from models_functions import *                           # Importation de toutes les fonctions de définition des modèles LSTM

# Récupération des tirages depuis le site de l'histoire des tirages
df_tirage = scrap_loto_numbers()

#LIGNE A ACTIVER SI ON VEUT TESTER LA PREDICTION DU DERNIER TIRAGE
df_tirage.drop(df_tirage.head(1).index,inplace=True)

# Affichage du dataframe des tirages
print(df_tirage)
df_tirage[['day','month_year','num0','num1','num2','num3','num4','chance']].head()

# Inversion de l'ordre des tirages pour avoir les plus anciens en premier
df = df_tirage.iloc[::-1]
df = df[['num0', 'num1', 'num2', 'num3', 'num4', 'chance']]
df.tail()

calculate_frequencies(df)

# Application des fonctions sur le dataframe
df['freq_num0'] = freq_val(df, 'num0')      # Calcul de la frequence du numéro 1
df['freq_num1'] = freq_val(df, 'num1')      # Calcul de la frequence du numéro 2
df['freq_num2'] = freq_val(df, 'num2')      # Calcul de la frequence du numéro 3
df['freq_num3'] = freq_val(df, 'num3')      # Calcul de la frequence du numéro 4
df['freq_num4'] = freq_val(df, 'num4')      # Calcul de la frequence du numéro 5
df['freq_chance'] = freq_val(df, 'chance')  # Calcul de la frequence du numéro chance
df['sum_diff'] = sum_diff(df)               # Somme de la différence au carré entre chaque couple de numéros successifs dans le tirage
df['pair_chance'] = is_pair_etoile(df)      # Détermine s'il y a plus de numéros pairs qu'impairs dans ce tirage
df['impair_chance'] = is_impair_etoile(df)  # Détermine s'il y a plus de numéros impairs que pairs dans ce tirage
df['pair'] = is_pair(df)                    # Vérifie si les 5 premiers numéros sont pairs
df['impair'] = is_impair(df)                # Vérifie si les 5 premiers numéros sont impairs
df['is_under_24'] = is_under(df, 24)        # Nombre de numéros en dessous de 24
df['is_under_40'] = is_under(df, 40)        # Nombre de numéros en dessous de 40

# Affichage des 6 premiers tirages
print(df.head(6))

# Moniteur pour arrêter l'entraînement
es = EarlyStopping(monitor='acc', mode='max', verbose=1, patience=100)

# Formatage des données pour le modèle LSTM
train, label, model = create_lstm_dataset(df)
print(train.shape)                                       # Affichage de la forme des données d'entraînement
print(label.shape)                                       # Affichage de la forme des étiquettes

# Entraînement du modèle LSTM
history = model.fit(train, label, batch_size=BATCHSIZE, epochs=EPOCH, verbose=2, callbacks=[es])

# Affichage de la courbe de perte d'entraînement
plt.plot(history.history['loss'])
plt.legend(['train_loss'])

# Prédiction
print(predict_next_loto_numbers(model, df))     # Prédiction des prochains numéros

# Affichage du graphique de l'entrainement
plt.show()
