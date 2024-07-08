import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import Database

class GestionNotesApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Gestion des Notes")
        self.create_widgets()
        self.update_listbox()

    def create_widgets(self):
        tk.Label(self.root, text="Matricule").grid(row=0, column=0)
        tk.Label(self.root, text="Nom").grid(row=1, column=0)
        tk.Label(self.root, text="Prénom").grid(row=2, column=0)
        tk.Label(self.root, text="Classe").grid(row=3, column=0)
        tk.Label(self.root, text="Matière").grid(row=4, column=0)
        tk.Label(self.root, text="Note").grid(row=5, column=0)

        self.entry_matricule = tk.Entry(self.root)
        self.entry_nom = tk.Entry(self.root)
        self.entry_prenom = tk.Entry(self.root)
        self.entry_classe = tk.Entry(self.root)
        self.entry_matiere = tk.Entry(self.root)
        self.entry_note = tk.Entry(self.root)

        self.entry_matricule.grid(row=0, column=1)
        self.entry_nom.grid(row=1, column=1)
        self.entry_prenom.grid(row=2, column=1)
        self.entry_classe.grid(row=3, column=1)
        self.entry_matiere.grid(row=4, column=1)
        self.entry_note.grid(row=5, column=1)

        tk.Button(self.root, text="Enregistrer", command=self.ajouter_etudiant).grid(row=6, column=0)
        tk.Button(self.root, text="Modifier", command=self.modifier_etudiant).grid(row=6, column=1)
        tk.Button(self.root, text="Supprimer", command=self.supprimer_etudiant).grid(row=6, column=2)
        tk.Button(self.root, text="Récupérer", command=self.recuperer_etudiant).grid(row=6, column=3)

        self.listbox = tk.Listbox(self.root)
        self.listbox.grid(row=0, column=2, rowspan=6)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)
            matricule = selected_item.split()[0]
            self.recuperer_etudiant_par_matricule(matricule)

    def ajouter_etudiant(self):
        matricule = self.entry_matricule.get()
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        classe = self.entry_classe.get()
        matiere = self.entry_matiere.get()
        note = self.entry_note.get()

        if matricule and nom and prenom and classe and matiere and note:
            self.db.ajouter_etudiant(matricule, nom, prenom, classe, matiere, note)
            messagebox.showinfo("Succès", "Étudiant ajouté avec succès")
            self.update_listbox()
            self.vider_champs()
        else:
            messagebox.showwarning("Attention", "Tous les champs sont requis")

    def modifier_etudiant(self):
        matricule = self.entry_matricule.get()
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        classe = self.entry_classe.get()
        matiere = self.entry_matiere.get()
        note = self.entry_note.get()

        if matricule:
            self.db.modifier_etudiant(matricule, nom, prenom, classe, matiere, note)
            messagebox.showinfo("Succès", "Étudiant modifié avec succès")
            self.update_listbox()
            self.vider_champs()
        else:
            messagebox.showwarning("Attention", "Le matricule est requis pour modifier")

    def supprimer_etudiant(self):
        matricule = self.entry_matricule.get()

        if matricule:
            self.db.supprimer_etudiant(matricule)
            messagebox.showinfo("Succès", "Étudiant supprimé avec succès")
            self.update_listbox()
            self.vider_champs()
        else:
            messagebox.showwarning("Attention", "Le matricule est requis pour supprimer")

    def recuperer_etudiant(self):
        matricule = self.entry_matricule.get()
        self.recuperer_etudiant_par_matricule(matricule)

    def recuperer_etudiant_par_matricule(self, matricule):
        if matricule:
            etudiant = self.db.recuperer_etudiant(matricule)
            if etudiant:
                self.entry_nom.delete(0, tk.END)
                self.entry_nom.insert(0, etudiant[1])
                self.entry_prenom.delete(0, tk.END)
                self.entry_prenom.insert(0, etudiant[2])
                self.entry_classe.delete(0, tk.END)
                self.entry_classe.insert(0, etudiant[3])
                self.entry_matiere.delete(0, tk.END)
                self.entry_matiere.insert(0, etudiant[4])
                self.entry_note.delete(0, tk.END)
                self.entry_note.insert(0, etudiant[5])
            else:
                messagebox.showwarning("Attention", "Étudiant non trouvé")
        else:
            messagebox.showwarning("Attention", "Le matricule est requis pour récupérer les informations")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        self.db.c.execute("SELECT matricule, nom FROM etudiants")
        for row in self.db.c.fetchall():
            self.listbox.insert(tk.END, f"{row[0]} - {row[1]}")

    def vider_champs(self):
        self.entry_matricule.delete(0, tk.END)
        self.entry_nom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_classe.delete(0, tk.END)
        self.entry_matiere.delete(0, tk.END)
        self.entry_note.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionNotesApp(root)
    root.mainloop()
