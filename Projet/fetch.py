import sqlite3
import csv
import requests

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
    
    # Fetch horaire with related conges and jour_de_travail information
    cursor.execute("""
        SELECT rh_HORAIRE.id_horaire, rh_CONGES.date AS date_conge, rh_JOUR_TRAVAIL.id_jour_de_travail 
        FROM rh_HORAIRE
        INNER JOIN rh_CONGES ON rh_HORAIRE.id_conges = rh_CONGES.id_conges
        INNER JOIN rh_JOUR_TRAVAIL ON rh_HORAIRE.id_jour_de_travail = rh_JOUR_TRAVAIL.id_jour_de_travail
    """)
    result = cursor.fetchall()
    conn.close()
    results_dict = [
        {
            "id_horaire": row[0],
            "date_conge": row[1],
            "id_jour_de_travail": row[2]
        }
        for row in result
    ]
    
    return results_dict


def fetch_conge():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_conges, date 
        FROM rh_CONGES
    """)
    result = cursor.fetchall()
    conn.close()
    results_dict = [
        {
            "id_conges": row[0],
            "date": row[1]
        }
        for row in result
    ]
    return results_dict

def fetch_jour_travail():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_jour_de_travail, heure_debut, heure_fin
        FROM rh_JOUR_TRAVAIL
    """)
    result = cursor.fetchall()
    conn.close()
    results_dict = [
        {
            "id_jour_de_travail": row[0],
            "heure_debut": row[1],
            "heure_fin": row[2]
        }
        for row in result
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

def add_employee_to_db(nas, nom, prenom, date_naissance, email, telephone, adresse=None, id_horaire=None, id_poste=None, id_salaire=None, id_succursale=None):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    try:
        # Insertion de l'employé dans la table info.INFO_PERSONNEL
        cursor.execute('''
            INSERT INTO info_PERSONNEL (NAS, nom, prenom, date_naissance, email, telephone, adresse)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nas, nom, prenom, date_naissance, email, telephone, adresse))
        
        id_individus = cursor.lastrowid

        # Insertion dans la table rh.EMPLOYE avec des valeurs NULL autorisées pour id_horaire, id_poste, id_salaire
        cursor.execute('''
            INSERT INTO rh_EMPLOYE (id_employe, id_horaire, id_poste, id_salaire, id_succursale)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_individus, id_horaire, id_poste, id_salaire, id_succursale))

        conn.commit()
        print("L'employé a été ajouté avec succès dans les deux tables.")
    except sqlite3.IntegrityError as e:
        print(f"Erreur d'intégrité : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        conn.close()

def delete_employee(employee_id):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM rh_EMPLOYE WHERE id_employe = ?
        """, (employee_id,))

        cursor.execute("""
            DELETE FROM rh_HORAIRE WHERE id_horaire = (SELECT id_horaire FROM rh_EMPLOYE WHERE id_employe = ?)
        """, (employee_id,))

        cursor.execute("""
            DELETE FROM rh_POSTE WHERE id_poste = (SELECT id_poste FROM rh_EMPLOYE WHERE id_employe = ?)
        """, (employee_id,))

        cursor.execute("""
            DELETE FROM rh_SALAIRE WHERE id_salaire = (SELECT id_salaire FROM rh_EMPLOYE WHERE id_employe = ?)
        """, (employee_id,))

        cursor.execute("""
            DELETE FROM succursales_SUCCURSALE WHERE id_succursale = (SELECT id_succursale FROM rh_EMPLOYE WHERE id_employe = ?)
        """, (employee_id,))

        cursor.execute("""
            DELETE FROM info_PERSONNEL WHERE id_individus = ?
        """, (employee_id,))

        conn.commit()

        print(f"Employee with ID {employee_id} has been deleted successfully.")
    
    finally:
        # Close the connection
        conn.close()
        
def insert_login_for_existing_employee(nas, visibilite, username, password = 12345):
    ''' USERNAME = EMAIL, PASSWORD = LEAVE AT DEFAULT VALUE'''
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_individus FROM info_PERSONNEL WHERE NAS = ?", (nas,))
        employee = cursor.fetchone()

        if employee:
            employee_id = employee[0]

            cursor.execute("""
                INSERT INTO info_LOGIN (id_employe, username, password, visibilite)
                VALUES (?, ?, ?, ?)
            """, (employee_id, username, password, visibilite))
            
            conn.commit()
            print(f"Login information for employee ID {employee_id} has been added successfully.")
        else:
            print("Employee not found with the provided NAS.")

    finally:
        conn.close()
        
def get_shop_id_by_name(shop_name):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    query = "SELECT id_entite FROM info_CIE WHERE nom = ?"
    cursor.execute(query, (shop_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

# Function to get all employees for a shop based on shop's ID
def get_employees_by_shop_id(shop_id):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Get all succursales for the given shop's id_entite
    query = """
        SELECT e.id_employe, e.id_horaire, e.id_poste, e.id_salaire, e.id_succursale 
        FROM rh_EMPLOYE e
        INNER JOIN succursales_SUCCURSALE s ON e.id_succursale = s.id_succursale
        WHERE s.id_info = ?
    """
    cursor.execute(query, (shop_id,))
    employees = cursor.fetchall()
    
    return employees

def get_employee_info_by_name(first_name, last_name):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    
    query = """
        SELECT * FROM info_PERSONNEL 
        WHERE nom = ? AND prenom = ?
    """
    cursor.execute(query, (first_name, last_name))
    employee_info = cursor.fetchone()
    
    return employee_info

def get_employee_info_by_id(employee_id):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    
    query = """
        SELECT * FROM info_PERSONNEL
        WHERE id_individus = ?
    """
    cursor.execute(query, (employee_id,))
    employee_info = cursor.fetchone()
    
    conn.close()
    return employee_info

def update_employee_info(employee_id, new_prenom, new_nom, new_telephone, new_adresse):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    try:
        query = """
            UPDATE info_PERSONNEL
            SET prenom = ?, nom = ?, telephone = ?, adresse = ?
            WHERE id_individus = ?
        """

        # Execute the query with the new values and employee_id
        cursor.execute(query, (new_prenom, new_nom, new_telephone, new_adresse, employee_id))

        # Commit the transaction
        conn.commit()

        print(f"Employee {employee_id} information updated successfully.")
        
    except sqlite3.Error as e:
        print(f"Error updating employee information: {e}")
        conn.rollback()  # Rollback if there is any error
    
    finally:
        # Close the connection
        conn.close()


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

def get_succursale_id_by_name(nom):
    conn = sqlite3.connect('erp.db') 
    cursor = conn.cursor()

    try:
        # Recherche dans info.INFO_CIE pour récupérer l'id_info en fonction du nom
        cursor.execute('''
            SELECT id_entite FROM info_CIE WHERE nom = ?
        ''', (nom,))
        
        # Récupérer l'id_entite (id_info)
        result = cursor.fetchone()
        
        if result:
            id_info = result[0]
            # Recherche dans succursales.SUCCURSALE avec l'id_info trouvé pour récupérer l'id_succursale
            cursor.execute('''
                SELECT id_succursale FROM succursales_SUCCURSALE WHERE id_info = ?
            ''', (id_info,))
            
            # Récupérer l'id_succursale
            succursale_result = cursor.fetchone()
            
            if succursale_result:
                return succursale_result[0]
            else:
                print("Aucune succursale trouvée pour cet id_info.")
                return None
        else:
            print("Aucun enregistrement trouvé pour ce nom dans INFO_CIE.")
            return None
            
    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")
        return None
    finally:
        conn.close()
        
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
####### COMMANDES ##########
############################
def fetch_commandes():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_commande, date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut
        FROM finances_COMMANDES
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def ajouter_commande(date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO finances_COMMANDES (date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut)
        VALUES (?, ?, ?, ?, ?)
    """, (date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut))
    conn.commit()
    conn.close()


def modifier_commande(id_commande, cout_apres_taxe, cout_avant_taxe, statut):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Vérification du statut
    cursor.execute("SELECT statut FROM finances_COMMANDES WHERE id_commande = ?", (id_commande,))
    current_statut = cursor.fetchone()

    if not current_statut or current_statut[0] == "Expédiée":
        conn.close()
        raise ValueError("Impossible de modifier une commande déjà expédiée.")

    # Mise à jour
    cursor.execute("""
        UPDATE finances_COMMANDES
        SET cout_apres_taxe = ?, cout_avant_taxe = ?, statut = ?
        WHERE id_commande = ?
    """, (cout_apres_taxe, cout_avant_taxe, statut, id_commande))
    conn.commit()
    conn.close()



def supprimer_commande(id_commande):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Vérification du statut et du délai
    cursor.execute("""
        SELECT statut, date_commande
        FROM finances_COMMANDES
        WHERE id_commande = ?
    """, (id_commande,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        raise ValueError("Commande introuvable.")

    statut, date_commande = result
    from datetime import datetime, timedelta

    if statut == "Expédiée":
        conn.close()
        raise ValueError("Impossible de supprimer une commande déjà expédiée.")

    # Vérifier si le délai de 7 jours est respecté
    if datetime.now() - datetime.strptime(date_commande, "%Y-%m-%d") > timedelta(days=7):
        conn.close()
        raise ValueError("Impossible de supprimer une commande après 7 jours.")

    # Suppression
    cursor.execute("DELETE FROM finances_COMMANDES WHERE id_commande = ?", (id_commande,))
    conn.commit()
    conn.close()

def get_acheteur_nom(id_acheteur):
    """
    Récupère le nom de l'acheteur (client, succursale ou entrepôt) en fonction de son ID.
    """
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Vérifier dans les clients
    cursor.execute("""
        SELECT info_PERSONNEL.nom || ' ' || info_PERSONNEL.prenom AS nom
        FROM clients_CLIENT
        INNER JOIN info_PERSONNEL ON clients_CLIENT.id_employe = info_PERSONNEL.id_individus
        WHERE clients_CLIENT.id_client = ?
    """, (id_acheteur,))
    result = cursor.fetchone()
    if result:
        conn.close()
        return result[0]  # Nom trouvé dans les clients

    # Vérifier dans les succursales
    cursor.execute("""
        SELECT info_CIE.nom
        FROM succursales_SUCCURSALE
        INNER JOIN info_CIE ON succursales_SUCCURSALE.id_info = info_CIE.id_entite
        WHERE succursales_SUCCURSALE.id_succursale = ?
    """, (id_acheteur,))
    result = cursor.fetchone()
    if result:
        conn.close()
        return result[0]  # Nom trouvé dans les succursales

    # Vérifier dans les entrepôts
    cursor.execute("""
        SELECT info_CIE.nom
        FROM entrepots_ENTREPOT
        INNER JOIN info_CIE ON entrepots_ENTREPOT.id_info = info_CIE.id_entite
        WHERE entrepots_ENTREPOT.id_entrepot = ?
    """, (id_acheteur,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]  # Nom trouvé dans les entrepôts

    return "Inconnu"  # Aucun nom trouvé


############################
####### TAXES ##########
############################
def fetch_taxes():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT TPS, TVQ FROM finances_TAXES")
    taxes = cursor.fetchone()
    conn.close()
    return taxes






##########################
######## CLIENT ##########
##########################
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


################################
######### GESTUON $$$ ##########
################################
def fetch_paiements_from_csv(filename="paiements.csv"):
    """
    Charge les paiements depuis un fichier CSV et les ajoute à la base de données.
    """
    global paiements  # Référence à la base de données existante
    
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                paiement = {
                    'date': row['Date'],
                    'salaire_brut': float(row['Salaire brut']),
                    'impots': float(row['Impôts']),
                    'taxes': float(row['Taxes']),
                    'salaire_net': float(row['Salaire net'])
                }
                paiements.append(paiement)
        print(f"Les paiements ont été chargés depuis le fichier {filename}.")
    except FileNotFoundError:
        print(f"Le fichier {filename} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement des paiements depuis le fichier : {e}")
        
def fetch_paiements_from_api(api_url="https://api.example.com/paiements"):
    """
    Récupère les paiements depuis une API et les ajoute à la base de données.
    """
    global paiements  # Référence à la base de données existante
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Si la requête échoue, une exception sera levée
        
        paiements_api = response.json()  # Supposons que l'API renvoie des données JSON
        
        for paiement_data in paiements_api:
            paiement = {
                'date': paiement_data['date'],  # Assurez-vous que les clés correspondent à la structure de l'API
                'salaire_brut': float(paiement_data['salaire_brut']),
                'impots': float(paiement_data['impots']),
                'taxes': float(paiement_data['taxes']),
                'salaire_net': float(paiement_data['salaire_net'])
            }
            paiements.append(paiement)
        print("Les paiements ont été récupérés depuis l'API.")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la récupération des paiements depuis l'API : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
