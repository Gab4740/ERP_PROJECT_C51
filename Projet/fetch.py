import sqlite3
import csv
import requests
from config import DB_PATH

def connect_to_db():
    return sqlite3.connect(DB_PATH)

############################
######## VISIBILITÉ ########
############################
def fetch_visibilite(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT visibilite FROM info_LOGIN WHERE username = ? and password = ?", (username, password))
    result = cursor.fetchone() 
    conn.close()
    return result[0] if result else None


############################
######## INVENTAIRE ########
############################
def fetch_inventaire():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventaires_INVENTAIRE") # changer la requête selon le besoin
    result = cursor.fetchall() # ou fetchone()
    conn.close()
    return result[0] if result else None


############################
######### HORAIRE ##########
############################
def fetch_horaire():
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rh_EMPLOYE") # changer la requête selon le besoin
    result = cursor.fetchall() # ou fetchone()
    conn.close()
    return result[0] if result else None

def add_employee_to_db(nas, nom, prenom, date_naissance, email, telephone, adresse=None, id_horaire=None, id_poste=None, id_salaire=None, id_succursale=None):
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
        SELECT * FROM info_PERSONNEL 
        WHERE nom = ? AND prenom = ?
    """
    cursor.execute(query, (first_name, last_name))
    employee_info = cursor.fetchone()
    
    return employee_info

def get_employee_info_by_id(employee_id):
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
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

    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
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
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def supprimer_succursale(nom_succursale):
    conn = connect_to_db()
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

    conn = connect_to_db()
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
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
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
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()



def supprimer_entrepot(nom_entrepot):
    conn = connect_to_db()
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
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_commande, date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut
        FROM finances_COMMANDES
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def ajouter_commande(date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO finances_COMMANDES (date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut)
            VALUES (?, ?, ?, ?, ?)
        """, (date_commande, cout_apres_taxe, cout_avant_taxe, id_acheteur, statut))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def modifier_commande(id_commande, cout_apres_taxe, cout_avant_taxe, statut):
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT TPS, TVQ FROM finances_TAXES")
    taxes = cursor.fetchone()
    conn.close()
    return taxes



############################
####### FOURNISSEUR ##########
############################
def fetch_fournisseurs():
    """
    Fetch all suppliers from the database.
    Returns:
        List of tuples (id_fournisseur, nom, adresse, telephone, email, type)
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
    SELECT f.id_fournisseur, i.nom, i.adresse, i.telephone, i.email, i.type
    FROM fournisseurs_FOURNISSEUR f
    INNER JOIN info_CIE i ON f.id_info = i.id_entite
    """
    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results




def fetch_fournisseur_details(fournisseur_id):
    """
    Fetch details of a specific supplier by its ID.
    Args:
        fournisseur_id (int): ID of the supplier.
    Returns:
        Dict containing details of the supplier or None if not found.
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
    SELECT f.id_fournisseur AS id, i.nom AS name, i.adresse AS address, 
           i.telephone AS phone, i.email AS email, i.type AS type
    FROM fournisseurs_FOURNISSEUR f
    INNER JOIN info_CIE i ON f.id_info = i.id_entite
    WHERE f.id_fournisseur = ?
    """
    cursor.execute(query, (fournisseur_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        keys = ["id", "name", "address", "phone", "email", "type"]
        return dict(zip(keys, result))
    return None



def add_fournisseur(name, address, phone, email, type):
    """
    Add a new supplier to the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Insert into `info_CIE`
        cursor.execute("""
        INSERT INTO info_CIE (nom, adresse, telephone, email, type)
        VALUES (?, ?, ?, ?, ?)
        """, (name, address, phone, email, type))
        id_info = cursor.lastrowid

        # Insert into `fournisseurs_FOURNISSEUR`
        cursor.execute("""
        INSERT INTO fournisseurs_FOURNISSEUR (id_info)
        VALUES (?)
        """, (id_info,))
        id_fournisseur = cursor.lastrowid

        conn.commit()
        return id_fournisseur
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_fournisseur(fournisseur_id, name, address, phone, email, type):
    """
    Update details for an existing supplier.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Update `info_CIE`
        cursor.execute("""
        UPDATE info_CIE
        SET nom = ?, adresse = ?, telephone = ?, email = ?, type = ?
        WHERE id_entite = (SELECT id_info FROM fournisseurs_FOURNISSEUR WHERE id_fournisseur = ?)
        """, (name, address, phone, email, type, fournisseur_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
        
        

def delete_fournisseur(fournisseur_id):
    """
    Delete a supplier from the database.
    Args:
        fournisseur_id (int): ID of the supplier to delete.
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Get id_info from fournisseurs_FOURNISSEUR
        cursor.execute("""
        SELECT id_info
        FROM fournisseurs_FOURNISSEUR
        WHERE id_fournisseur = ?
        """, (fournisseur_id,))
        id_info = cursor.fetchone()

        if not id_info:
            raise ValueError(f"Fournisseur ID {fournisseur_id} not found.")

        # Delete from fournisseurs_FOURNISSEUR
        cursor.execute("""
        DELETE FROM fournisseurs_FOURNISSEUR
        WHERE id_fournisseur = ?
        """, (fournisseur_id,))

        # Delete from info_CIE
        cursor.execute("""
        DELETE FROM info_CIE
        WHERE id_entite = ?
        """, (id_info[0],))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()






##########################
######## CLIENT ##########
##########################
def fetch_client():

    conn = connect_to_db()
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
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
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
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def supprimer_client(id_client):
    conn = connect_to_db()
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
    conn = connect_to_db()
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


############################
##### CUSTOM FIELD #########
############################
def add_custom_field(entity_type, field_name, field_type, is_required):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO custom_fields (entity_type, field_name, field_type, is_required)
            VALUES (?, ?, ?, ?)
        """, (entity_type, field_name, field_type, is_required))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Erreur SQL : {e}")
    finally:
        conn.close()
    
    
def fetch_custom_fields(entity_type=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    if entity_type:
        cursor.execute("""
            SELECT id, field_name, field_type, is_required
            FROM custom_fields
            WHERE entity_type = ?
        """, (entity_type,))
    else:
        cursor.execute("""
            SELECT id, field_name, field_type, is_required
            FROM custom_fields
        """)
    fields = cursor.fetchall()
    conn.close()
    return fields


def save_custom_field_values(entity_type, entity_id, field_values):
    """
    Enregistre les valeurs des champs dynamiques pour une entité donnée.
    :param entity_type: Type de l'entité (par ex., "Commande").
    :param entity_id: ID de l'entité principale (commande, client, etc.).
    :param field_values: Liste de tuples (field_id, valeur).
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    for field_id, value in field_values:
        cursor.execute("""
            INSERT INTO custom_field_values (entity_type, entity_id, field_id, value)
            VALUES (?, ?, ?, ?)
        """, (entity_type, entity_id, field_id, value))
    conn.commit()
    conn.close()




def fetch_custom_field_values(entity_type, entity_id, as_dict=False):
    """
    Récupère les valeurs des champs dynamiques pour une entité donnée.
    :param entity_type: Type de l'entité (par ex., "Commande").
    :param entity_id: ID de l'entité principale (commande, client, etc.).
    :param as_dict: Si True, retourne un dictionnaire {field_id: valeur}.
                    Si False, retourne une liste de tuples [(field_name, valeur)].
    :return: Un dictionnaire ou une liste en fonction de `as_dict`.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cf.field_name, cf.id, cfv.value
        FROM custom_field_values cfv
        INNER JOIN custom_fields cf ON cf.id = cfv.field_id
        WHERE cfv.entity_type = ? AND cfv.entity_id = ?
    """, (entity_type, entity_id))
    results = cursor.fetchall()
    conn.close()

    if as_dict:
        # Retourne un dictionnaire {field_id: valeur}
        return {field_id: value for _, field_id, value in results}
    else:
        # Retourne une liste de tuples [(field_name, valeur)]
        return [(field_name, value) for field_name, _, value in results]




def update_custom_field_values(entity_type, entity_id, field_values):
    """
    Met à jour ou insère les valeurs des champs dynamiques pour une entité donnée.
    :param entity_type: Type de l'entité (par ex., "Commande").
    :param entity_id: ID de l'entité principale (commande, client, etc.).
    :param field_values: Liste de tuples (field_id, valeur).
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    for field_id, value in field_values:
        # Vérifier si une valeur existe déjà pour ce champ
        cursor.execute("""
            SELECT id FROM custom_field_values
            WHERE entity_type = ? AND entity_id = ? AND field_id = ?
        """, (entity_type, entity_id, field_id))
        existing = cursor.fetchone()

        if existing:
            # Mettre à jour si une valeur existe déjà
            cursor.execute("""
                UPDATE custom_field_values
                SET value = ?
                WHERE entity_type = ? AND entity_id = ? AND field_id = ?
            """, (value, entity_type, entity_id, field_id))
        else:
            # Insérer une nouvelle valeur si elle n'existe pas
            cursor.execute("""
                INSERT INTO custom_field_values (entity_type, entity_id, field_id, value)
                VALUES (?, ?, ?, ?)
            """, (entity_type, entity_id, field_id, value))

    conn.commit()
    conn.close()


def delete_custom_field(field_id):
    """
    Supprime un champ personnalisé et ses valeurs associées.
    :param field_id: ID du champ personnalisé à supprimer.
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    # Supprimer les valeurs associées au champ
    cursor.execute("""
        DELETE FROM custom_field_values
        WHERE field_id = ?
    """, (field_id,))

    # Supprimer le champ personnalisé lui-même
    cursor.execute("""
        DELETE FROM custom_fields
        WHERE id = ?
    """, (field_id,))

    conn.commit()

    conn.close()


############################
######### PRODUITS ##########
############################

def fetch_products():
    """Fetch all products with basic details."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                p.id_produit, p.nom_produit, p.qte_inventaire, p.prix_unitaire, 
                p.description, p.categorie, i.id_inventaire, f.id_fournisseur, d.id_departement
            FROM produits_PRODUIT p
            LEFT JOIN inventaires_INVENTAIRE i ON p.id_inventaire = i.id_inventaire
            LEFT JOIN fournisseurs_FOURNISSEUR f ON p.id_fournisseur = f.id_fournisseur
            LEFT JOIN info_DEPARTEMENT d ON p.id_departement = d.id_departement
        """)
        products = [
            {
                "id": row[0],
                "name": row[1],
                "stock": row[2],
                "price": row[3],
                "description": row[4],
                "category": row[5],
                "inventory_id": row[6],
                "supplier_id": row[7],
                "department_id": row[8]
            }
            for row in cursor.fetchall()
        ]
    finally:
        conn.close()

    return products




def fetch_product_details(product_id):
    """Fetch detailed information about a specific product."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                p.id_produit, p.nom_produit, p.description, p.categorie, p.prix_unitaire, 
                p.qte_inventaire, n.nom
            FROM produits_PRODUIT p
            LEFT JOIN info_CIE n ON p.id_inventaire = n.id_entite
            WHERE p.id_produit = ?
        """, (product_id,))
        row = cursor.fetchone()

        if row:
            product = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "category": row[3],
                "price": row[4],
                "stock": row[5],
                "inventory_id": row[6]
                # "supplier_id": row[6],
                # "department_id": row[7],
                # "private_label": bool(row[8])
            }
            return product
    finally:
        conn.close()

    return None




def add_product(name, description, category, price, stock, inventory_id, supplier_id=None, department_id=None, private_label=False):
    """Add a new product to the database."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO produits_PRODUIT (
                nom_produit, description, categorie, prix_unitaire, qte_inventaire, 
                id_inventaire, id_fournisseur, id_departement, marque_propre
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, category, price, stock, inventory_id, supplier_id, department_id, private_label))
        conn.commit()
    finally:
        conn.close()


        

def transfer_product(product_id, source_inventory_id, target_inventory_id, quantity):
    """Transfer a product between inventories."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Check if enough stock exists in the source inventory
        cursor.execute("""
            SELECT qte_inventaire
            FROM produits_PRODUIT
            WHERE id_produit = ? AND id_inventaire = ?
        """, (product_id, source_inventory_id))
        stock = cursor.fetchone()

        if not stock or stock[0] < quantity:
            raise ValueError("Stock insuffisant dans l'inventaire source.")

        # Decrease stock in source inventory
        cursor.execute("""
            UPDATE produits_PRODUIT
            SET qte_inventaire = qte_inventaire - ?
            WHERE id_produit = ? AND id_inventaire = ?
        """, (quantity, product_id, source_inventory_id))

        # Check if the product already exists in the target inventory
        cursor.execute("""
            SELECT id_produit
            FROM produits_PRODUIT
            WHERE id_produit = ? AND id_inventaire = ?
        """, (product_id, target_inventory_id))
        existing_product = cursor.fetchone()

        if existing_product:
            # Increase stock in the target inventory
            cursor.execute("""
                UPDATE produits_PRODUIT
                SET qte_inventaire = qte_inventaire + ?
                WHERE id_produit = ? AND id_inventaire = ?
            """, (quantity, product_id, target_inventory_id))
        else:
            # Create a new product entry in the target inventory
            cursor.execute("""
                INSERT INTO produits_PRODUIT (nom_produit, description, categorie, 
                                              prix_unitaire, qte_inventaire, id_inventaire, 
                                              id_fournisseur, id_departement, marque_propre)
                SELECT nom_produit, description, categorie, prix_unitaire, ?, ?, 
                       id_fournisseur, id_departement, marque_propre
                FROM produits_PRODUIT
                WHERE id_produit = ?
            """, (quantity, target_inventory_id, product_id))

        conn.commit()
    finally:
        conn.close()



############################
######### INVENTAIRES ##########
############################
def fetch_inventories():
    """Fetch all inventory locations."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id_inventaire, id_emplacement
            FROM inventaires_INVENTAIRE
        """)
        inventories = [
            {"id": row[0], "location": row[1]} for row in cursor.fetchall()
        ]
    finally:
        conn.close()

    return inventories


def fetch_low_stock_products(threshold=10):
    """Fetch products with stock below a certain threshold."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id_produit, nom_produit, qte_inventaire
            FROM produits_PRODUIT
            WHERE qte_inventaire < ?
        """, (threshold,))
        products = [
            {"id": row[0], "name": row[1], "stock": row[2]} for row in cursor.fetchall()
        ]
    finally:
        conn.close()

    return products


def order_products(product_ids):
    """Simulate ordering products."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Example logic to increase stock
        for product_id in product_ids:
            cursor.execute("""
                UPDATE produits_PRODUIT
                SET qte_inventaire = qte_inventaire + 50
                WHERE id_produit = ?
            """, (product_id,))

        conn.commit()
    finally:
        conn.close()

def fetch_inventory_id(location_id):
    """Fetch the inventory ID associated with a specific location."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:

        query = """
            SELECT nom FROM info_CIE
            WHERE id_entite = ?
        """

        cursor.execute(query, (location_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def fetch_inventory_nom(location):
    """Fetch the inventory ID associated with a specific location."""
    conn = connect_to_db()
    cursor = conn.cursor()

    try:

        query = """
            SELECT id_entite FROM info_CIE
            WHERE nom = ?
        """

        cursor.execute(query, (location,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()



