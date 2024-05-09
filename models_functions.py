from keras.models import Sequential                                                         # Pour les modèles séquentiels
from keras.layers import LSTM, Dense, Bidirectional, TimeDistributed, RepeatVector, Flatten # Pour les couches du réseau de neurones LSTM
import numpy as np                                                                          # Pour la manipulation des tableaux
import pandas as pd                                                                         # Pour la manipulation des données
from sklearn.preprocessing import StandardScaler                                            # Pour la mise à l'échelle des données

# Paramètre du modèle
NB_LABEL_FEATURES    = 6              # Nombre de caractéristiques dans les étiquettes
UNITS               = 100            # Nombre d'unités dans la couche LSTM
BATCHSIZE           = 30             # Taille des lots
EPOCH               = 1500           # Nombre d'entraînements maximum
OPTIMIZER           = 'adam'         # Optimiseur à utiliser
LOSS                = 'mae'          # Fonction de perte à utiliser
DROPOUT             = 0.1            # Taux de dropout
WINDOW_LENGTH       = 12             # Longueur de la fenêtre (nombre de tirages à considérer, ici 12 tirages car 3 tirages par semaine soit un test sur 1 mois)

# Architecture du modèle
def define_model(nb_features):
    """
    Définit l'architecture du modèle LSTM.
    """
    # Initialisation du rnn
    model = Sequential()
    # Ajout de la premiere couche lstm
    model.add(LSTM(UNITS, input_shape=(WINDOW_LENGTH, nb_features), return_sequences=True))
    model.add(LSTM(UNITS, dropout=0.1, return_sequences=False))
    # Ajout de la couche de sortie
    model.add(Dense(NB_LABEL_FEATURES))
    model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=['acc'])
    return model

def define_bidirectionnel_model(nb_features):
    """
    Définit l'architecture du modèle LSTM bidirectionnel.
    """
    model = Sequential()
    model.add(Bidirectional(LSTM(100, dropout=0.2, return_sequences=True), input_shape=(WINDOW_LENGTH, nb_features)))
    model.add(LSTM(50, return_sequences=True))
    model.add(LSTM(100, dropout=0.1))
    model.add(Dense(NB_LABEL_FEATURES))
    model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=['acc'])
    return model

def define_autoencoder_model(nb_features):
    """
    Définit l'architecture du modèle LSTM autoencodeur.
    """
    model = Sequential()
    model.add(LSTM(100, input_shape=(WINDOW_LENGTH, nb_features), return_sequences=True))
    model.add(LSTM(50, return_sequences=False))
    model.add(RepeatVector(WINDOW_LENGTH))
    model.add(LSTM(100, dropout=0.1, return_sequences=True))
    model.add(LSTM(50, return_sequences=True))
    model.add(TimeDistributed(Dense(nb_features)))
    model.add(Flatten())
    model.add(Dense(NB_LABEL_FEATURES))
    model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=['acc'])
    return model

# Fonction de formatage des données en entrée du LSTM
def create_lstm_dataset(df):
    """
    Prépare les données pour l'entraînement du modèle LSTM.
    """
    number_of_rows = df.shape[0]                        # Taille du dataset
    nb_features    = df.shape[1]                        # Nombre de caractéristiques
    scaler = StandardScaler().fit(df.values)            # Mise à l'échelle des données
    transformed_dataset = scaler.transform(df.values)   # Transformation des données
    transformed_df = pd.DataFrame(data=transformed_dataset, index=df.index)

    # Tableau de tableau de taille (number_of_rows-WINDOW_LENGTH) et WINDOW_LENGTH lignes, NB_FEATURES colonnes
    train = np.empty([number_of_rows-WINDOW_LENGTH, WINDOW_LENGTH, nb_features], dtype=float)

    label = np.empty([number_of_rows-WINDOW_LENGTH, NB_LABEL_FEATURES], dtype=float)
    for i in range(0, number_of_rows-WINDOW_LENGTH):
        train[i] = transformed_df.iloc[i:i+WINDOW_LENGTH, 0: nb_features]
        label[i] = transformed_df.iloc[i+WINDOW_LENGTH: i+WINDOW_LENGTH+1, 0:NB_LABEL_FEATURES]

    # Définition du modèle LSTM
    model = define_model(nb_features)

    return train, label, model

def predict_next_loto_numbers(model, df):
    # Prédiction basée sur les 12 derniers tirages
    last_draws = df.tail(WINDOW_LENGTH)

    scaler = StandardScaler().fit(df.values)                                   # Récupération des 12 derniers tirages
    scaled_to_predict = StandardScaler().fit(df.values).transform(last_draws)  # Mise à l'échelle des données pour la prédiction
    scaled_predicted_output_1 = model.predict(np.array([scaled_to_predict]))   # Prédiction

    # Prédiction effective
    tom = df.tail(WINDOW_LENGTH).iloc[:,0:6]                 # Sélection des données pour la prédiction
    scaler = StandardScaler().fit(df.iloc[:,0:6])            # Mise à l'échelle des données
    scaled_to_predict = scaler.transform(tom)                # Mise à l'échelle des données pour la prédiction
    predicted_output = model.predict(np.array([scaled_to_predict]))  # Prédiction des prochains numéros
    predicted_numbers = scaler.inverse_transform(predicted_output).astype(int)[0]  # Inversion de la mise à l'échelle
    return predicted_numbers
