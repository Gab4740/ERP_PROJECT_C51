DROP SCHEMA IF EXISTS info CASCADE;
DROP SCHEMA IF EXISTS rh CASCADE;
DROP SCHEMA IF EXISTS clients CASCADE;
DROP SCHEMA IF EXISTS finances CASCADE;
DROP SCHEMA IF EXISTS produits CASCADE;
DROP SCHEMA IF EXISTS fournisseurs CASCADE;
DROP SCHEMA IF EXISTS succursales CASCADE;
DROP SCHEMA IF EXISTS entrepots CASCADE;
DROP SCHEMA IF EXISTS inventaires CASCADE;
DROP SCHEMA IF EXISTS stats CASCADE;
DROP SCHEMA IF EXISTS periode CASCADE;

CREATE SCHEMA info;
CREATE SCHEMA rh;
CREATE SCHEMA clients;
CREATE SCHEMA finances;
CREATE SCHEMA produits;
CREATE SCHEMA fournisseurs;
CREATE SCHEMA succursales;
CREATE SCHEMA entrepots;
CREATE SCHEMA inventaires;
CREATE SCHEMA stats;
CREATE SCHEMA periode;

CREATE SEQUENCE info.id_individus_seq START with 10000 INCREMENT BY 1;
CREATE SEQUENCE info.id_entite_seq START with 20000 INCREMENT BY 1;
CREATE SEQUENCE rh.id_salaire_seq START with 30000 INCREMENT BY 1;
CREATE SEQUENCE rh.id_conges_seq START with 40000 INCREMENT BY 1;
CREATE SEQUENCE rh.id_jour_de_travail_seq START with 50000 INCREMENT BY 1;
CREATE SEQUENCE rh.id_horaire_seq START with 60000 INCREMENT BY 1;
CREATE SEQUENCE info.id_departement_seq START with 70000 INCREMENT BY 1;
CREATE SEQUENCE rh.id_poste_seq START with 80000 INCREMENT BY 1;
CREATE SEQUENCE rh.id_formation_seq START with 100000 INCREMENT BY 1;
CREATE SEQUENCE rh.id_absent_seq START with 110000 INCREMENT BY 1;
CREATE SEQUENCE clients.id_client_seq START with 120000 INCREMENT BY 1;
CREATE SEQUENCE succursales.id_succursale_seq START with 130000 INCREMENT BY 1;
CREATE SEQUENCE entrepots.id_entrepot_seq START with 140000 INCREMENT BY 1;
CREATE SEQUENCE finances.id_commande_seq START with 150000 INCREMENT BY 1;
CREATE SEQUENCE finances.id_facture_seq START with 160000 INCREMENT BY 1;
CREATE SEQUENCE produits.id_retour_seq START with 170000 INCREMENT BY 1;
CREATE SEQUENCE inventaires.id_inventaire_seq START with 180000 INCREMENT BY 1;
CREATE SEQUENCE fournisseurs.id_fournisseur_seq START with 190000 INCREMENT BY 1;
CREATE SEQUENCE produits.id_produit_seq START with 200000 INCREMENT BY 1;
CREATE SEQUENCE produits.id_controle_seq START with 210000 INCREMENT BY 1;
CREATE SEQUENCE stats.id_stats_client_seq START with 220000 INCREMENT BY 1;
CREATE SEQUENCE periode.id_quartile_client_seq START with 230000 INCREMENT BY 1;
CREATE SEQUENCE periode.id_mois_client_seq START with 240000 INCREMENT BY 1;
CREATE SEQUENCE periode.id_date_client_seq START with 250000 INCREMENT BY 1;
CREATE SEQUENCE periode.id_periode_seq START with 260000 INCREMENT BY 1;
CREATE SEQUENCE stats.id_stats_succursale_seq START with 270000 INCREMENT BY 1;
CREATE SEQUENCE stats.id_stats_produit_seq START with 280000 INCREMENT BY 1;
CREATE SEQUENCE finances.id_budget_seq START with 290000 INCREMENT BY 1;
CREATE SEQUENCE stats.id_statistiques_seq START with 300000 INCREMENT BY 1;
CREATE SEQUENCE entrepots.id_stock_entrepot_seq START with 310000 INCREMENT BY 1;
CREATE SEQUENCE produits.id_audit_seq START with 320000 INCREMENT BY 1;
CREATE SEQUENCE produits.id_devis_seq START with 330000 INCREMENT BY 1;
CREATE SEQUENCE produits.id_appel_seq START with 340000 INCREMENT BY 1;
CREATE SEQUENCE finances.id_paiement_seq START with 350000 INCREMENT BY 1;

CREATE TABLE info.INFO_PERSONNEL (
    id_individus SERIAL PRIMARY KEY,
    NAS VARCHAR(32) UNIQUE CHECK (NAS ~ '^\d{3}-\d{3}-\d{3}$'),
    nom VARCHAR(32) NOT NULL,
    prenom VARCHAR(32) NOT NULL,
    date_naissance DATE CHECK(date_naissance >= '1900-01-01'),
    email VARCHAR(64) CHECK (POSITION('@' IN email) > 0),
    telephone VARCHAR(15) CHECK (LENGTH(telephone) <= 15),
    adresse VARCHAR(32),
    date_creation DATE DEFAULT CURRENT_DATE
);

CREATE TABLE info.INFO_CIE (
    id_entite SERIAL PRIMARY KEY,
    nom VARCHAR(32) NOT NULL,
    adresse VARCHAR(64),
    telephone VARCHAR(15) CHECK (LENGTH(telephone) <= 15),
    email VARCHAR(64) CHECK (POSITION('@' IN email) > 0),
    type VARCHAR(32)
);

CREATE TABLE rh.SALAIRE (
    id_salaire SERIAL PRIMARY KEY,
    salaire_h FLOAT NOT NULL,
    impot_pourcent FLOAT NOT NULL,
    date_paie_emit DATE CHECK(date_paie_emit >= '1900-01-01'),
    montant MONEY CHECK(montant >= 0::money)
);

CREATE TABLE rh.CONGES (
    id_conges SERIAL PRIMARY KEY,
    date DATE CHECK(date >= '1900-01-01')
);

CREATE TABLE rh.JOUR_TRAVAIL (
    id_jour_de_travail SERIAL PRIMARY KEY,
    heure_debut TIMESTAMP NOT NULL,
    heure_fin TIMESTAMP NOT NULL
);

CREATE TABLE rh.HORAIRE (
    id_horaire SERIAL PRIMARY KEY,
    id_conges INTEGER REFERENCES rh.CONGES(id_conges),
    id_jour_de_travail INTEGER REFERENCES rh.JOUR_TRAVAIL(id_jour_de_travail)
);

CREATE TABLE info.DEPARTEMENT (
    id_departement SERIAL PRIMARY KEY,
    nom VARCHAR(32) NOT NULL,
    description VARCHAR(200),
    numero_extension INT
);

CREATE TABLE rh.POSTE (
    id_poste SERIAL PRIMARY KEY,
    nom_poste VARCHAR(64) NOT NULL,
    id_departement INTEGER REFERENCES info.DEPARTEMENT(id_departement)
);

CREATE TABLE rh.EMPLOYE (
    id_employe SERIAL PRIMARY KEY REFERENCES info.INFO_PERSONNEL(id_individus),
    id_horaire INTEGER REFERENCES rh.HORAIRE(id_horaire),
    id_poste INTEGER REFERENCES rh.POSTE(id_poste),
    id_salaire INTEGER REFERENCES rh.SALAIRE(id_salaire)
);

CREATE TABLE info.LOGIN (
	id_employe SERIAL PRIMARY KEY REFERENCES info.INFO_PERSONNEL(id_individus),
	username VARCHAR(64) NOT NULL,
	password VARCHAR(64) NOT NULL,
	visibilite INT NOT NULL
);



CREATE TABLE rh.FORMATION (
    id_formation SERIAL PRIMARY KEY,
    id_employe INTEGER REFERENCES rh.EMPLOYE(id_employe),
    date_debut DATE CHECK(date_debut >= '1900-01-01'),
    date_fin DATE CHECK(date_fin >= '1900-01-01'),
    statut VARCHAR(200) NOT NULL
);


CREATE TABLE rh.ABSENTEISMES (
    id_absent SERIAL PRIMARY KEY,
    id_employe INTEGER REFERENCES rh.EMPLOYE(id_employe),
    date_debut DATE CHECK(date_debut >= '1900-01-01'),
    date_fin DATE CHECK(date_fin >= '1900-01-01'),
    motif VARCHAR(200)
);


CREATE TABLE clients.CLIENT (
    id_client SERIAL PRIMARY KEY,
    id_employe INTEGER REFERENCES info.INFO_PERSONNEL(id_individus),
    type INT NOT NULL
);

CREATE TABLE succursales.SUCCURSALE (
    id_succursale SERIAL PRIMARY KEY,
    id_info INTEGER REFERENCES info.INFO_CIE(id_entite)
);


CREATE TABLE entrepots.ENTREPOT (
    id_entrepot SERIAL PRIMARY KEY,
    id_info INTEGER REFERENCES info.INFO_CIE(id_entite)
);

CREATE TABLE finances.COMMANDES (
    id_commande SERIAL PRIMARY KEY,
    date_commande DATE NOT NULL,
    cout_apres_taxe FLOAT NOT NULL,
    cout_avant_taxe FLOAT NOT NULL,
    id_acheteur INTEGER,
    FOREIGN KEY (id_acheteur) REFERENCES entrepots.ENTREPOT(id_entrepot),
    FOREIGN KEY (id_acheteur) REFERENCES succursales.SUCCURSALE(id_succursale)
);


CREATE TABLE finances.FACTURE (
    id_facture SERIAL PRIMARY KEY,
    id_commande INTEGER REFERENCES finances.COMMANDES(id_commande)
);


CREATE TABLE produits.RETOURS (
    id_retour SERIAL PRIMARY KEY,
    id_facture INTEGER REFERENCES finances.FACTURE(id_facture),
    date DATE CHECK(date >= '1900-01-01'),
    motif VARCHAR(200)
);

CREATE TABLE inventaires.INVENTAIRE (
    id_inventaire SERIAL PRIMARY KEY,
    id_emplacement INTEGER,
    FOREIGN KEY (id_emplacement) REFERENCES info.DEPARTEMENT(id_departement),
    FOREIGN KEY (id_emplacement) REFERENCES entrepots.ENTREPOT(id_entrepot),
    FOREIGN KEY (id_emplacement) REFERENCES succursales.SUCCURSALE(id_succursale)
);

CREATE TABLE fournisseurs.FOURNISSEUR (
    id_fournisseur SERIAL PRIMARY KEY,
    id_info INTEGER REFERENCES info.INFO_CIE(id_entite)
);

CREATE TABLE produits.PRODUIT (
    id_produit SERIAL PRIMARY KEY,
    prix_unitaire MONEY CHECK(prix_unitaire >= 0::money),
    nom_produit VARCHAR(32) NOT NULL,
    description VARCHAR(200),
    categorie VARCHAR(32),
    qte_inventaire INT NOT NULL,
    id_inventaire INTEGER REFERENCES inventaires.INVENTAIRE(id_inventaire),
    marge_profit FLOAT,
    id_fournisseur INTEGER REFERENCES fournisseurs.FOURNISSEUR(id_fournisseur),
    id_departement INTEGER REFERENCES info.DEPARTEMENT(id_departement),
    marque_propre BOOLEAN
);

CREATE TABLE produits.PRODUITS_ACHETES (
    id_produit INTEGER REFERENCES produits.PRODUIT(id_produit),
    id_commande INTEGER REFERENCES finances.COMMANDES(id_commande),
    qte_achete INT CHECK(qte_achete >= 1),
    PRIMARY KEY (id_produit, id_commande)
);



CREATE TABLE produits.CONTROLE_QUALITE (
    id_controle SERIAL PRIMARY KEY,
    id_produit INTEGER REFERENCES produits.PRODUIT(id_produit),
    type VARCHAR(32) NOT NULL,
    date DATE CHECK(date >= '1900-01-01'),
    resultat VARCHAR(32),
    description VARCHAR(200)
);



CREATE TABLE stats.STATS_CLIENT (
    id_stats_client SERIAL PRIMARY KEY,
    id_client INTEGER REFERENCES clients.CLIENT(id_client),
    total_depense MONEY CHECK(total_depense >= 0::money),
    nombre_visite INT NOT NULL
);


CREATE TABLE periode.QUARTILE (
    id_quartile SERIAL PRIMARY KEY,
    nom_quartile VARCHAR(32) NOT NULL
);


CREATE TABLE periode.MOIS (
    id_mois SERIAL PRIMARY KEY,
    id_quartile INTEGER REFERENCES periode.QUARTILE(id_quartile),
    nom_mois VARCHAR(15) NOT NULL
);


CREATE TABLE periode.DATE (
    id_date SERIAL PRIMARY KEY,
    id_mois INTEGER REFERENCES periode.MOIS(id_mois),
    jour_du_mois INT NOT NULL
);


CREATE TABLE periode.PERIODE (
    id_periode SERIAL PRIMARY KEY,
    date_debut DATE CHECK(date_debut >= '1900-01-01'),
    date_fin DATE CHECK(date_fin >= '1900-01-01')
);

CREATE TABLE stats.VENTE_PAR_SUCCURSALE (
    id_stats_succursale SERIAL PRIMARY KEY,
    id_succursale INTEGER REFERENCES succursales.SUCCURSALE(id_succursale),
    qte_commande INT CHECK(qte_commande >= 1),
    total MONEY CHECK(total >= 0::money),
    id_periode INTEGER REFERENCES periode.PERIODE(id_periode)
);


CREATE TABLE stats.VENTE_PAR_PRODUIT (
    id_stats_produit SERIAL PRIMARY KEY,
    id_produit INTEGER REFERENCES produits.PRODUIT(id_produit),
    qte_vendu INT CHECK(qte_vendu >= 1),
    total MONEY CHECK(total >= 0::money),
    id_periode INTEGER REFERENCES periode.PERIODE(id_periode)
);


CREATE TABLE finances.BUDGET (
    id_budget SERIAL PRIMARY KEY,
    id_periode INTEGER REFERENCES periode.PERIODE(id_periode),
    total MONEY CHECK(total >= 0::money),
    id_entite INTEGER,
    FOREIGN KEY (id_entite) REFERENCES info.DEPARTEMENT(id_departement),
    FOREIGN KEY (id_entite) REFERENCES entrepots.ENTREPOT(id_entrepot),
    FOREIGN KEY (id_entite) REFERENCES succursales.SUCCURSALE(id_succursale),
    montant_total MONEY CHECK(montant_total >= 0::money),
    montant_utilise MONEY CHECK(montant_utilise >= 0::money)
);


CREATE TABLE stats.STATISTIQUES (
    id_statistiques SERIAL PRIMARY KEY,
    id_stats INTEGER,
    FOREIGN KEY (id_stats) REFERENCES stats.STATS_CLIENT(id_stats_client),
    FOREIGN KEY (id_stats) REFERENCES stats.VENTE_PAR_SUCCURSALE(id_stats_succursale),
    FOREIGN KEY (id_stats) REFERENCES stats.VENTE_PAR_PRODUIT(id_stats_produit)
);


CREATE TABLE finances.TAXES (
    TPS FLOAT NOT NULL,
    TVQ FLOAT NOT NULL
);


CREATE TABLE entrepots.STOCK_ENTREPOT (
    id_stock_entrepot SERIAL PRIMARY KEY,
    id_produit INTEGER REFERENCES produits.PRODUIT(id_produit),
    id_entrepot INTEGER REFERENCES entrepots.ENTREPOT(id_entrepot),
    quantite INT NOT NULL,
    date_ajout DATE CHECK(date_ajout >= '1900-01-01')
);


CREATE TABLE produits.AUDITS_INSPECTIONS (
    id_audit SERIAL PRIMARY KEY,
    id_produit INTEGER REFERENCES produits.PRODUIT(id_produit),
    type VARCHAR(32) NOT NULL,
    date DATE CHECK(date >= '1900-01-01'),
    resultat VARCHAR(200)
);


CREATE TABLE produits.DEVIS (
    id_devis SERIAL PRIMARY KEY,
    id_fournisseur INTEGER REFERENCES fournisseurs.FOURNISSEUR(id_fournisseur),
    id_produit INTEGER REFERENCES produits.PRODUIT(id_produit),
    prix MONEY CHECK(prix >= 0::money),
    quantite INT NOT NULL,
    date DATE CHECK(date >= '1900-01-01')
);


CREATE TABLE produits.APPEL_OFFRES (
    id_appel SERIAL PRIMARY KEY,
    id_fournisseur INTEGER REFERENCES fournisseurs.FOURNISSEUR(id_fournisseur),
    id_produit INTEGER REFERENCES produits.PRODUIT(id_produit),
    quantite INT NOT NULL,
    date_limite DATE CHECK(date_limite >= '1900-01-01')
);


CREATE TABLE finances.PAIEMENTS (
    id_paiement SERIAL PRIMARY KEY,
    id_fournisseur INTEGER REFERENCES fournisseurs.FOURNISSEUR(id_fournisseur),
    date DATE CHECK(DATE >= '1900-01-01'),
    montant MONEY CHECK(montant >= 0::money)
);

INSERT INTO info.INFO_PERSONNEL VALUES(nextval('info.id_individus_seq'), '999-999-999', 'Admin', 'Admin', '1900-01-01', 'admin@admin.ca', '514-999-9999', '');

INSERT INTO info.LOGIN VALUES((SELECT id_individus FROM info.INFO_PERSONNEL WHERE nom='Admin' ), 'admin', 'admin', 0);

--select * from info.INFO_PERSONNEL
--select * from info.LOGIN

