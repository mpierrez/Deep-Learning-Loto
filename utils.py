# Liste de nombres pairs et impairs
pairs = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
impairs = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]

# Fonction de vérification de nombres en dessous d'une certaine valeur pour les 5 premiers numéros, sauf celui de chance
def is_under(data, number):
    """
    Vérifie si les 5 premiers numéros sont inférieurs à une certaine valeur.
    """
    return ((data['num0'] <= number).astype(int) +
            (data['num1'] <= number).astype(int) +
            (data['num2'] <= number).astype(int) +
            (data['num3'] <= number).astype(int) +
            (data['num4'] <= number).astype(int))

# Fonction de vérification de nombres pairs pour les 5 premiers numéros sauf celui de chance
def is_pair(data):
    """
    Vérifie si les 5 premiers numéros sont pairs.
    """
    return ((data['num0'].isin(pairs)).astype(int) +
            (data['num1'].isin(pairs)).astype(int) +
            (data['num2'].isin(pairs)).astype(int) +
            (data['num3'].isin(pairs)).astype(int) +
            (data['num4'].isin(pairs)).astype(int))

# Fonction de vérification de nombres impairs pour les 5 premiers numéros sauf celui de chance
def is_impair(data):
    """
    Vérifie si les 5 premiers numéros sont impairs.
    """
    return ((data['num0'].isin(impairs)).astype(int) +
            (data['num1'].isin(impairs)).astype(int) +
            (data['num2'].isin(impairs)).astype(int) +
            (data['num3'].isin(impairs)).astype(int) +
            (data['num4'].isin(impairs)).astype(int))

# Fonction de vérification de nombres pairs pour le numéro de chance
def is_pair_etoile(data):
    """
    Vérifie si le numéro chance est pair.
    """
    return (data['chance'].isin(pairs)).astype(int)

# Fonction de vérification de nombres impairs pour le numéro de chance
def is_impair_etoile(data):
    """
    Vérifie si le numéro chance est impair.
    """
    return (data['chance'].isin(impairs)).astype(int)

# Fonction de calcul de la somme de la différence au carré des 5 premiers numéros, sauf celui de chance
def sum_diff(data):
    """
    Calcule la somme des différences au carré entre les 5 premiers numéros.
    """
    return ((data['num1'] - data['num0'])**2 +
            (data['num2'] - data['num1'])**2 +
            (data['num3'] - data['num2'])**2 +
            (data['num4'] - data['num3'])**2)

# Fonction de calcul de la fréquence de tirage de chaque numéro
def freq_val(data, column):
    """
    Calcule la fréquence d'apparition de chaque valeur dans une colonne.
    """
    # On convertit la colonne en liste
    tab = data[column].values.tolist()
    freqs = []
    pos = 1

    # Pour chaque élément dans la liste
    for e in tab:
        # On compte le nombre d'occurrences et on l'ajoute à la liste des fréquences
        freqs.append(tab[0:pos].count(e))
        pos += 1

    return freqs
