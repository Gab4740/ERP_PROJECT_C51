import sqlite3


def fetch_visibilite(username, password):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT visibilite FROM info_LOGIN WHERE username = ? and password = ?", (username, password))
    result = cursor.fetchone() 
    conn.close()
    return result[0] if result else None



def fetch_inventaire():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventaires_INVENTAIRE") # changer la requête selon le besoin
    result = cursor.fetchall() # ou fetchone()
    conn.close()
    return result[0] if result else None



def fetch_produit():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits_PRODUIT") # changer la requête selon le besoin
    results = cursor.fetchall() 
    conn.close()
    results_dict = [
        {
            "id_produit": result[0],
            "prix_unitaire": result[1],
            "nom_produit": result[2],
            "description": result[3],
            "categorie": result[4],
            "qte_inventaire": result[5],
            "marge_profit": result[6],
            "marque_propre": bool(result[9]) 
        }
        for result in results
    ]
    return results_dict



def fetch_employe():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rh_EMPLOYE") # changer la requête selon le besoin
    result = cursor.fetchall() # ou fetchone()
    conn.close()
    return result[0] if result else None



def fetch_succursale():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM succursales_SUCCURSALE") # changer la requête selon le besoin
    result = cursor.fetchall() # ou fetchone()
    conn.close()
    return result[0] if result else None



def fetch_commande():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM finances_COMMANDES") # changer la requête selon le besoin
    results = cursor.fetchall() 
    conn.close()
    results_dict = [
        {
            "id_commande": result[0],
            "date_commande ": result[1],
            "cout_apres_taxe": result[2],
            "cout_avant_taxe": result[3]
        }
        for result in results
    ]
    return results_dict
