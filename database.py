import sqlite3

class Database:
    def __init__(self, db_name='etudiants.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.creer_table()

    def creer_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS etudiants
                          (matricule TEXT PRIMARY KEY, nom TEXT, prenom TEXT, classe TEXT, matiere TEXT, note REAL)''')
        self.conn.commit()

    def ajouter_etudiant(self, matricule, nom, prenom, classe, matiere, note):
        self.c.execute("INSERT INTO etudiants VALUES (?, ?, ?, ?, ?, ?)",
                       (matricule, nom, prenom, classe, matiere, note))
        self.conn.commit()

    def modifier_etudiant(self, matricule, nom, prenom, classe, matiere, note):
        self.c.execute('''UPDATE etudiants SET nom=?, prenom=?, classe=?, matiere=?, note=?
                          WHERE matricule=?''', (nom, prenom, classe, matiere, note, matricule))
        self.conn.commit()

    def supprimer_etudiant(self, matricule):
        self.c.execute("DELETE FROM etudiants WHERE matricule=?", (matricule,))
        self.conn.commit()

    def recuperer_etudiant(self, matricule):
        self.c.execute("SELECT * FROM etudiants WHERE matricule=?", (matricule,))
        etudiant = self.c.fetchone()
        return etudiant

    def __del__(self):
        self.conn.close()
