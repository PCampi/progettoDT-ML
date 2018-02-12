"""Modulo per la distanza di Jaccard."""
import re

import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_similarity_score


def jaccard(setA, setB):
    """Calcola la distanza di Jaccard tra due set di tokens."""
    if len(setA) == 0 and len(setB) == 0:
        return 1.0

    similarity = len(setA.intersection(setB)) / len(setA.union(setB))
    return similarity


def clean_name(name):
    """Pulisce il nome togliendo Rep, Dem, Is, St..."""
    tmp = re.sub(r"[,()]", r"", name)
    tmp = re.sub(r"Is\.", "Islands", tmp)
    tmp = re.sub(r"Dem\.", "Democratic", tmp)
    tmp = re.sub(r"Rep\.", "Republic", tmp)
    tmp = re.sub(r"Fed\.", "Federated", tmp)
    tmp = re.sub(r"St\.", "Saint", tmp)
    tmp = re.sub(r"SAR", "Special Administrative Region", tmp)

    return tmp


nomi = pd.read_csv(
    "./Dataset/Puliti_da_usare/Country-codes-v1.csv", sep=";", quotechar='"')
carbone = pd.read_csv(
    "./Dataset/Puliti_da_usare/Charcoal_UNData.csv", sep=",", quotechar='"')
carburanti = pd.read_csv(
    "./Dataset/Puliti_da_usare/Gas and Diesel 2011-2016.csv",
    sep=";",
    quotechar='"')


def clean_column(dataset, nome_campo):
    """Pulisce tutti i nomi di un dataset."""
    colonna_da_pulire = dataset[nome_campo]
    pulita = [clean_name(nome) for nome in colonna_da_pulire]

    return pulita


def split_name(name):
    """Splitta un nome su spazio."""
    return name.split(' ')


nomi['official_name_en'] = clean_column(nomi, 'official_name_en')

carbone['Country or Area'] = clean_column(carbone, 'Country or Area')
carburanti['Country or Area'] = clean_column(carburanti, 'Country or Area')

nomi['name_tokens'] = [split_name(name) for name in nomi['official_name_en']]

carbone['name_tokens'] = [
    split_name(name) for name in carbone['Country or Area']
]

carburanti['name_tokens'] = [
    split_name(name) for name in carburanti['Country or Area']
]


def jaccard_matrix(true_tokens, tokens_to_match):
    """Make a matrix of shape (len(true_tokens), len(tokens_to_match))
    where matrix[i, j] = jaccard(true_tokens[i], tokens_to_match[j])
    """
    result = np.zeros((len(true_tokens), len(tokens_to_match)))

    for row_index, row in enumerate(true_tokens):
        for col_index, col in enumerate(tokens_to_match):
            result[row_index, col_index] = jaccard(set(row), set(col))

    return result


def match_codici(nomi_paesi, dataset, matrice_jaccard):
    """Matcha i paesi in base alla distanza di Jaccard."""
    max_indexes = np.argmax(matrice_jaccard, axis=0)

    def get_codice_paese(riga):
        return nomi_paesi.loc[riga, 'ISO3166-1-Alpha-3']

    codici_paese = [get_codice_paese(index) for index in max_indexes]

    return codici_paese


match_nomi_carbone = jaccard_matrix(nomi['name_tokens'],
                                    carbone['name_tokens'])
match_nomi_carburanti = jaccard_matrix(nomi['name_tokens'],
                                       carburanti['name_tokens'])

codici_carbone = match_codici(nomi, carbone, match_nomi_carbone)
codici_carburanti = match_codici(nomi, carburanti, match_nomi_carburanti)

carbone['Code'] = codici_carbone
carburanti['Code'] = codici_carburanti

carbone = carbone.drop(columns=['name_tokens'])
carburanti = carburanti.drop(columns=['name_tokens'])

carbone.to_csv("./Dataset/finali/Carbone.csv", index=False)
# np.savetxt("./Dataset/finali/Carbone2.csv", carbone[:, 1:])
carburanti.to_csv("./Dataset/finali/Carburanti.csv", index=False)
