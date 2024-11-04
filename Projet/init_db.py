import sqlite3

def initialize_db():
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
    CREATE TABLE IF NOT EXISTS LOGIN (
        id_employe INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        visibilite INTEGER NOT NULL,
        FOREIGN KEY(id_employe) REFERENCES info_PERSONNEL(id_individus)
    )""")
    
    # Add initial user
    cursor.execute("""
    INSERT OR IGNORE INTO info_PERSONNEL (NAS, nom, prenom, date_naissance, email, telephone, adresse)
    VALUES ('999-999-999', 'Admin', 'Admin', '1900-01-01', 'admin@admin.ca', '514-999-9999', '123 Admin St')
    """)
    
    # Add initial login entry
    cursor.execute("""
    INSERT OR IGNORE INTO LOGIN (id_employe, username, password, visibilite)
    VALUES ((SELECT id_individus FROM info_PERSONNEL WHERE nom='Admin'), 'admin', 'admin', 0)
    """)
    
    conn.commit()
    conn.close()

initialize_db()
