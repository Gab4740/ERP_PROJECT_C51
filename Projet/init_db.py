import os
import sqlite3

def initialize_db():
    if not os.path.exists('erp.db'):
        conn = sqlite3.connect('erp.db')
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS info_PERSONNEL (
            id_individus INTEGER PRIMARY KEY AUTOINCREMENT,
            NAS TEXT UNIQUE,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance DATE,
            email TEXT,
            telephone TEXT,
            adresse TEXT,
            date_creation DATE DEFAULT CURRENT_DATE
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS info_CIE (
            id_entite INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            adresse TEXT,
            telephone TEXT,
            email TEXT,
            type TEXT
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_SALAIRE (
            id_salaire INTEGER PRIMARY KEY AUTOINCREMENT,
            salaire_h REAL NOT NULL,
            impot_pourcent REAL NOT NULL,
            date_paie_emit DATE,
            montant REAL
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_CONGES (
            id_conges INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_JOUR_TRAVAIL (
            id_jour_de_travail INTEGER PRIMARY KEY AUTOINCREMENT,
            heure_debut TIMESTAMP NOT NULL,
            heure_fin TIMESTAMP NOT NULL
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_HORAIRE (
            id_horaire INTEGER PRIMARY KEY AUTOINCREMENT,
            id_conges INTEGER,
            id_jour_de_travail INTEGER,
            FOREIGN KEY (id_conges) REFERENCES rh_CONGES(id_conges),
            FOREIGN KEY (id_jour_de_travail) REFERENCES rh_JOUR_TRAVAIL(id_jour_de_travail)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS info_DEPARTEMENT (
            id_departement INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            numero_extension INTEGER
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_POSTE (
            id_poste INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_poste TEXT NOT NULL,
            id_departement INTEGER,
            FOREIGN KEY (id_departement) REFERENCES info_DEPARTEMENT(id_departement)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_EMPLOYE (
            id_employe INTEGER PRIMARY KEY,
            id_horaire INTEGER,
            id_poste INTEGER,
            id_salaire INTEGER,
            id_succursale INTEGER,
            FOREIGN KEY (id_employe) REFERENCES info_PERSONNEL(id_individus),
            FOREIGN KEY (id_horaire) REFERENCES rh_HORAIRE(id_horaire),
            FOREIGN KEY (id_poste) REFERENCES rh_POSTE(id_poste),
            FOREIGN KEY (id_salaire) REFERENCES rh_SALAIRE(id_salaire),
            FOREIGN KEY (id_succursale) REFERENCES succursales_SUCCURSALE(id_succursale)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS info_LOGIN (
            id_employe INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            visibilite INTEGER NOT NULL,
            FOREIGN KEY (id_employe) REFERENCES info_PERSONNEL(id_individus)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_FORMATION (
            id_formation INTEGER PRIMARY KEY AUTOINCREMENT,
            id_employe INTEGER,
            date_debut DATE,
            date_fin DATE,
            statut TEXT NOT NULL,
            FOREIGN KEY (id_employe) REFERENCES rh_EMPLOYE(id_employe)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rh_ABSENTEISMES (
            id_absent INTEGER PRIMARY KEY AUTOINCREMENT,
            id_employe INTEGER,
            date_debut DATE,
            date_fin DATE,
            motif TEXT,
            FOREIGN KEY (id_employe) REFERENCES rh_EMPLOYE(id_employe)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients_CLIENT (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            id_employe INTEGER,
            type TEXT NOT NULL,
            FOREIGN KEY (id_employe) REFERENCES info_PERSONNEL(id_individus)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS succursales_SUCCURSALE (
            id_succursale INTEGER PRIMARY KEY AUTOINCREMENT,
            id_info INTEGER,
            FOREIGN KEY (id_info) REFERENCES info_CIE(id_entite)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entrepots_ENTREPOT (
            id_entrepot INTEGER PRIMARY KEY AUTOINCREMENT,
            id_info INTEGER,
            FOREIGN KEY (id_info) REFERENCES info_CIE(id_entite)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS finances_COMMANDES (
            id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            date_commande DATE NOT NULL,
            cout_apres_taxe REAL NOT NULL,
            cout_avant_taxe REAL NOT NULL,
            id_acheteur INTEGER,
            FOREIGN KEY (id_acheteur) REFERENCES entrepots_ENTREPOT(id_entrepot),
            FOREIGN KEY (id_acheteur) REFERENCES succursales_SUCCURSALE(id_succursale)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS finances_FACTURE (
            id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande INTEGER,
            FOREIGN KEY (id_commande) REFERENCES finances_COMMANDES(id_commande)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produits_RETOURS (
            id_retour INTEGER PRIMARY KEY AUTOINCREMENT,
            id_facture INTEGER,
            date DATE,
            motif TEXT,
            FOREIGN KEY (id_facture) REFERENCES finances_FACTURE(id_facture)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventaires_INVENTAIRE (
            id_inventaire INTEGER PRIMARY KEY AUTOINCREMENT,
            id_emplacement INTEGER,
            FOREIGN KEY (id_emplacement) REFERENCES info_DEPARTEMENT(id_departement),
            FOREIGN KEY (id_emplacement) REFERENCES entrepots_ENTREPOT(id_entrepot),
            FOREIGN KEY (id_emplacement) REFERENCES succursales_SUCCURSALE(id_succursale)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fournisseurs_FOURNISSEUR (
            id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
            id_info INTEGER,
            FOREIGN KEY (id_info) REFERENCES info_CIE(id_entite)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produits_PRODUIT (
            id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
            prix_unitaire REAL,
            nom_produit TEXT NOT NULL,
            description TEXT,
            categorie TEXT,
            qte_inventaire INTEGER NOT NULL,
            id_inventaire INTEGER,
            marge_profit REAL,
            id_fournisseur INTEGER,
            id_departement INTEGER,
            marque_propre BOOLEAN,
            FOREIGN KEY (id_inventaire) REFERENCES inventaires_INVENTAIRE(id_inventaire),
            FOREIGN KEY (id_fournisseur) REFERENCES fournisseurs_FOURNISSEUR(id_fournisseur),
            FOREIGN KEY (id_departement) REFERENCES info_DEPARTEMENT(id_departement)
        )""")
        
        
        
        
        
        # Add initial user
        cursor.execute("""
        INSERT OR IGNORE INTO info_PERSONNEL (NAS, nom, prenom, date_naissance, email, telephone, adresse)
        VALUES ('999-999-999', 'Admin', 'Admin', '1900-01-01', 'admin@admin.ca', '514-999-9999', '123 Admin St')
        """)
        
        # Add initial login entry
        cursor.execute("""
        INSERT OR IGNORE INTO info_LOGIN (id_employe, username, password, visibilite)
        VALUES ((SELECT id_individus FROM info_PERSONNEL WHERE nom='Admin'), 'admin', 'admin', 0)
        """)
        
        conn.commit()
        conn.close()

initialize_db()
