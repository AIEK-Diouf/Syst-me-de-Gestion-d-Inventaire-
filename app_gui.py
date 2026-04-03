import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from S_G_I import *

class AppInventaire:
    def __init__(self, root):
        self.root = root
        self.root.title("S.G.I - Gestion d'Inventaire")
        self.root.geometry("1100x650")
        self.afficher_login()

    def nettoyer_fenetre(self):
        for w in self.root.winfo_children(): w.destroy()

    def trier_colonne(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0].split()[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        for i, (v, k) in enumerate(l): self.tree.move(k, '', i)
        self.tree.heading(col, command=lambda: self.trier_colonne(col, not reverse))

    def afficher_login(self):
        self.nettoyer_fenetre()
        f = tk.Frame(self.root); f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(f, text="ACCÈS SGI", font=("Arial", 14, "bold")).pack(pady=10)
        self.e_u = tk.Entry(f); self.e_u.pack(pady=5)
        self.e_p = tk.Entry(f, show="*"); self.e_p.pack(pady=5)
        tk.Button(f, text="Entrer", bg="#2ecc71", command=self.login).pack(pady=10)

    def login(self):
        if self.e_u.get() == "ADMINE" and self.e_p.get() == "1234": self.choix_init()
        else: messagebox.showerror("Erreur", "Identifiants faux")

    def choix_init(self):
        self.nettoyer_fenetre()
        tk.Button(self.root, text="📁 Importer CSV", command=self.import_csv).pack(pady=10)
        tk.Button(self.root, text="🆕 Nouveau", command=self.menu_principal).pack(pady=10)

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path and importer_donner(path): self.menu_principal()

    def menu_principal(self):
        self.nettoyer_fenetre()
        # Barre latérale
        b = tk.Frame(self.root, bg="#ecf0f1", width=220); b.pack(side="left", fill="y")
        
        # Recherche
        tk.Label(b, text="🔍 RECHERCHE", bg="#ecf0f1").pack(pady=(10,0))
        self.search = tk.Entry(b); self.search.pack(padx=10, pady=5)
        self.search.bind("<KeyRelease>", lambda e: self.refresh())

        # Boutons
        for t, c in [("➕ Ajouter", self.form_add), ("📝 Modifier", self.form_edit), 
                     ("❌ Supprimer", self.delete), ("💾 Sauver", self.save)]:
            tk.Button(b, text=t, command=c).pack(fill="x", padx=10, pady=5)
        
        tk.Button(b, text="📊 Valeur", command=lambda: messagebox.showinfo("Bilan", f"{calculer_valeur_totale()} MAD")).pack(fill="x", padx=10, pady=5)
        tk.Button(b, text="⬅ Retour", command=self.choix_init, bg="#bdc3c7").pack(side="bottom", fill="x", padx=10, pady=10)

        # Tableau
        cols = ("Nom", "Prix", "Catégorie", "Stock", "Alerte")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c, command=lambda _c=c: self.trier_colonne(_c, False))
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        term = self.search.get().lower()
        for n in Produit:
            if term in n:
                p, c = Produit[n]
                q, s = Stock.get(n, 0), Seuils.get(n, 0)
                self.tree.insert("", "end", values=(n.upper(), f"{p} MAD", c, q, "⚠️" if q<=s else "OK"))

    def form_add(self): self.popup("Ajouter")
    def form_edit(self):
        sel = self.tree.selection()
        if sel: self.popup("Modifier", self.tree.item(sel[0])['values'])
        else: messagebox.showwarning("!", "Sélectionnez un produit")

    def popup(self, title, data=None):
        w = tk.Toplevel(self.root)
        w.title(title)
        ents = {}
        champs = ["Nom", "Prix", "Catégorie", "Stock", "Seuil"]
        
        for i, f in enumerate(champs):
            tk.Label(w, text=f).pack()
            e = tk.Entry(w)
            e.pack()
            ents[f] = e
            
            if data:
                # Si on modifie, on nettoie l'affichage pour l'utilisateur
                val = str(data[i]).replace(" MAD", "")
                if i == 4: # Si c'est la colonne Alerte
                    # On récupère la vraie valeur dans le dictionnaire au lieu du texte 'OK'
                    nom_key = data[0].lower()
                    val = Seuils.get(nom_key, 0)
                
                e.insert(0, val)
                if i == 0: e.config(state='disabled')

        def go():
            if ajouter_modifier_produit(ents["Nom"].get(), ents["Prix"].get(), 
                                      ents["Catégorie"].get(), ents["Stock"].get(), 
                                      ents["Seuil"].get()):
                self.refresh() # On utilise votre fonction refresh existante
                w.destroy()
            else:
                messagebox.showerror("Erreur", "Veuillez entrer des chiffres valides.")

        tk.Button(w, text="Valider", command=go, bg="#3498db", fg="white").pack(pady=10)

    def delete(self):
        sel = self.tree.selection()
        if sel and supprimer_produit(self.tree.item(sel[0])['values'][0].lower()): self.refresh()

    def save(self):
        p = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if p and sauvgard_donner(p): messagebox.showinfo("OK", "Sauvegardé")

if __name__ == "__main__":
    r = tk.Tk(); AppInventaire(r); r.mainloop()