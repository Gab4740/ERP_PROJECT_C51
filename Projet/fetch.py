import sqlite3

############################
######## VISIBILITÉ ########
############################
def fetch_visibilite(username, password):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT visibilite FROM info_LOGIN WHERE username = ? and password = ?", (username, password))
    result = cursor.fetchone() 
    conn.close()
    return result[0] if result else None


############################
######## INVENTAIRE ########
############################
def fetch_inventaire():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventaires_INVENTAIRE") # changer la requête selon le besoin
    result = cursor.fetchall() # ou fetchone()
    conn.close()
    return result[0] if result else None


############################
######## PRODUIT ###########
############################
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

############################
######### HORAIRE ##########
############################
def fetch_horaire():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rh.HORAIRE")
    result = cursor.fetchall()
    conn.close()
    results_dict = [
        {
            "id_horaire": result[0],
            "id_conges": result[1],
            "id_jour_de_travail": result[2]
        }
        for result in result
    ]
    return results_dict

############################
######## EMPLOYÉ ###########
############################
def fetch_employe():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rh_EMPLOYE") # changer la requête selon le besoin
    result = cursor.fetchall() # ou fetchone()
    conn.close()
    return result[0] if result else None

<<<<<<< Updated upstream
def ajouter_employe():
    pass

=======
def ajouter_horaire(id_employe, id_jour_de_travail, heure_debut, heure_fin):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Insertion de l'horaire dans la table HORAIRE
    cursor.execute("""
        INSERT INTO rh.HORAIRE (id_employe, id_jour_de_travail, heure_debut, heure_fin)
        VALUES (?, ?, ?, ?)
    """, (id_employe, id_jour_de_travail, heure_debut, heure_fin))

    conn.commit()
    print(f"Horaire ajouté pour l'employé {id_employe} le jour {id_jour_de_travail}.")

    conn.close()
    
>>>>>>> Stashed changes

############################
###### SUCCURSALE ##########
############################
def fetch_succursale():

    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT succursales_SUCCURSALE.id_succursale, info_CIE.*
        FROM succursales_SUCCURSALE
        INNER JOIN info_CIE
        ON succursales_SUCCURSALE.id_info = info_CIE.id_entite
    """)
    
    result = cursor.fetchall()  # Récupère tous les résultats
    conn.close()
    
    return result


def ajouter_succursale(nom, adresse, telephone, email, type_cie):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Ajouter les informations de l'entité (INFO_CIE)
    cursor.execute("""
        INSERT INTO info_CIE (nom, adresse, telephone, email, type)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, adresse, telephone, email, type_cie))
    
    # Récupérer l'ID de l'entité insérée
    id_entite = cursor.lastrowid
    
    # Ajouter la succursale associée
    cursor.execute("""
        INSERT INTO succursales_SUCCURSALE (id_info)
        VALUES (?)
    """, (id_entite,))
    
    conn.commit()
    print(f"Succursale '{nom}' ajoutée avec succès.")

    conn.close()


def supprimer_succursale(nom_succursale):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Trouver l'id_info correspondant au nom de la succursale
    cursor.execute("""
        SELECT id_entite FROM info_CIE WHERE nom = ?
    """, (nom_succursale,))
    id_info = cursor.fetchone()

    if not id_info:
        raise ValueError(f"Aucune succursale trouvée avec le nom '{nom_succursale}'.")

    id_info = id_info[0]  # Extraire la valeur de id_info

    # Supprimer d'abord dans succursales_SUCCURSALE
    cursor.execute("""
        DELETE FROM succursales_SUCCURSALE WHERE id_info = ?
    """, (id_info,))

    # Ensuite, supprimer dans info_CIE
    cursor.execute("""
        DELETE FROM info_CIE WHERE id_entite = ?
    """, (id_info,))

    conn.commit()
    print(f"Succursale '{nom_succursale}' supprimée avec succès.")
    conn.close()




############################
######## ENTREPÔT ##########
############################
def fetch_entrepot():

    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT entrepots_ENTREPOT.id_entrepot, info_CIE.*
        FROM entrepots_ENTREPOT
        INNER JOIN info_CIE
        ON entrepots_ENTREPOT.id_info = info_CIE.id_entite
    """)
    
    result = cursor.fetchall()  # Récupère tous les résultats
    conn.close()
    
    return result

def ajouter_entrepot(nom, adresse, telephone, email, type_cie):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Ajouter les informations de l'entité (INFO_CIE)
    cursor.execute("""
        INSERT INTO info_CIE (nom, adresse, telephone, email, type)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, adresse, telephone, email, type_cie))
    
    # Récupérer l'ID de l'entité insérée
    id_entite = cursor.lastrowid
    
    # Ajouter l'entrepot associé
    cursor.execute("""
        INSERT INTO entrepots_ENTREPOT (id_info)
        VALUES (?)
    """, (id_entite,))
    
    conn.commit()
    print(f"Entrepôt '{nom}' ajouté avec succès.")

    conn.close()



def supprimer_entrepot(nom_entrepot):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Trouver l'id_info correspondant au nom de la succursale
    cursor.execute("""
        SELECT id_entite FROM info_CIE WHERE nom = ?
    """, (nom_entrepot,))
    id_info = cursor.fetchone()

    if not id_info:
        raise ValueError(f"Aucun entrepôt trouvée avec le nom '{nom_entrepot}'.")

    id_info = id_info[0]  # Extraire la valeur de id_info

    # Supprimer d'abord dans entrepots_ENTREPOT
    cursor.execute("""
        DELETE FROM entrepots_ENTREPOT WHERE id_info = ?
    """, (id_info,))

    # Ensuite, supprimer dans info_CIE
    cursor.execute("""
        DELETE FROM info_CIE WHERE id_entite = ?
    """, (id_info,))

    conn.commit()
    print(f"Entrepôt '{nom_entrepot}' supprimé avec succès.")
    conn.close()




############################
######## COMMANDE ##########
############################
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






############################
######## CLIENT ############
############################
def fetch_client():

    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT clients_CLIENT.id_client, clients_CLIENT.type, info_PERSONNEL.*
        FROM clients_CLIENT
        INNER JOIN info_PERSONNEL
        ON clients_CLIENT.id_employe = info_PERSONNEL.id_individus
    """)
    
    result = cursor.fetchall()  # Récupère tous les résultats
    conn.close()
    
    return result


def ajouter_client(nas, nom, prenom, datenaissance, email, telephone, adresse, type):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Ajouter les informations de l'entité (INFO_CIE)
    cursor.execute("""
        INSERT INTO info_PERSONNEL (NAS, nom, prenom, date_naissance, email, telephone, adresse)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nas, nom, prenom, datenaissance, email, telephone, adresse))
    
    # Récupérer l'ID de l'entité insérée
    id_employe = cursor.lastrowid
    
    # Ajouter la succursale associée
    cursor.execute("""
        INSERT INTO clients_CLIENT (id_employe, type)
        VALUES (?, ?)
    """, (id_employe, type))
    
    conn.commit()
    print(f"Client '{nom}' '{prenom}' ajouté avec succès.")

    conn.close()


def supprimer_client(id_client):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Trouver l'ID de l'employé associé au client
    cursor.execute("""
        SELECT id_employe FROM clients_CLIENT WHERE id_client = ?
    """, (id_client,))
    id_employe = cursor.fetchone()

    if not id_employe:
        raise ValueError(f"Aucun client trouvé avec l'ID '{id_client}'.")

    id_employe = id_employe[0]

    # Supprimer le client de clients_CLIENT
    cursor.execute("""
        DELETE FROM clients_CLIENT WHERE id_client = ?
    """, (id_client,))

    # Supprimer les informations personnelles de info_PERSONNEL
    cursor.execute("""
        DELETE FROM info_PERSONNEL WHERE id_individus = ?
    """, (id_employe,))

    conn.commit()
    print(f"Client avec ID '{id_client}' supprimé avec succès.")
    conn.close()


def update_client(id_client, nas, nom, prenom, date_naissance, email, telephone, adresse, type_client):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()


    # Trouver l'ID de l'employé associé au client
    cursor.execute("""
        SELECT id_employe FROM clients_CLIENT WHERE id_client = ?
    """, (id_client,))
    id_employe = cursor.fetchone()

    if not id_employe:
        raise ValueError(f"Aucun client trouvé avec l'ID '{id_client}'.")

    id_employe = id_employe[0]

    # Mettre à jour les informations dans info_PERSONNEL
    cursor.execute("""
        UPDATE info_PERSONNEL
        SET NAS = ?, nom = ?, prenom = ?, date_naissance = ?, email = ?, telephone = ?, adresse = ?
        WHERE id_individus = ?
    """, (nas, nom, prenom, date_naissance, email, telephone, adresse, id_employe))

    # Mettre à jour le type du client dans clients_CLIENT
    cursor.execute("""
        UPDATE clients_CLIENT
        SET type = ?
        WHERE id_client = ?
    """, (type_client, id_client))

    conn.commit()
    print(f"Client avec ID '{id_client}' mis à jour avec succès.")

    conn.close()





