import os
import csv
from datetime import datetime

# --- STRUCTURE DE DONNÉES (BASE DE DONNÉES LOCALE) ---
# Utilisation de 3 dictionnaires synchronisés par le 'NOM' du produit
Produit = {}  # Stocke { 'Nom': (Prix, Catégorie) }
Stock = {}    # Stocke { 'Nom': Quantité }
Seuils = {}   # Stocke { 'Nom': Seuil_Alerte }

###1
def ajouter_produit_stock():
    """Demande les infos à l'utilisateur et remplit les dictionnaires."""
    NOM = input("Nom du produit : ")

    while True:
        try:
            PRIX = float(input("Prix du produit en MAD : "))
            break
        except ValueError:
            print("Erreur : La valeur du prix doit être un nombre (ex: 12.50).")

    CAT = input("Catégorie du produit : ")
    while True :
        try:
            QTE = int(input("Stock du produit : "))
            break
        except ValueError:
            print("Erreur : La quantité doit être un nombre entier.")
    while True:
        try:
            LIMITE = int(input("Seuil d'alerte : "))
            break
        except ValueError:
            print("Erreur : Le seuil doit être un nombre entier.")

    #Enregistrement final
    Produit[NOM] = (PRIX, CAT)
    Stock[NOM] = QTE
    Seuils[NOM] = LIMITE
    print(f"\n✅ Le produit '{NOM}' a été ajouté avec succès.")


###
def supprime_produit_stock():
    """Vérifie l'existence d'un produit et le retire de partout."""
    NOM = input("Nom du produit à supprimer : ")
    if NOM in Produit:
        del Produit[NOM]
        del Stock[NOM]
        if NOM in Seuils: del Seuils[NOM]
        print(f"Le produit {NOM} a été supprimé avec succès.")
    else:
        print("Le produit n'existe pas, impossible de le supprimer.")

###
def modifer_produit_stock():
    """Met à jour les valeurs pour une clé (NOM) déjà existante."""
    NOM = input("Nom du produit à modifier : ")
    if NOM in Produit:
        while True:
            try:
                PRIX = float(input("Nouveau prix : "))
                break
            except ValueError:
                print("Erreur : La valeur du prix doit être un nombre (ex: 12.50).")

        CAT = input("Nouvelle catégorie : ")
        while True:
            try:
                QTE = int(input("Nouveau stock : "))
                break
            except ValueError:
                print("Erreur : La quantité doit être un nombre entier.")
        #Enregistrement final
        Produit[NOM] = (PRIX, CAT)
        Stock[NOM] = QTE
        print(f"\n✅ Le produit '{NOM}' a été modifier avec succès.")
###
def verifier_stock():
    """Compare le stock actuel au seuil limite défini à l'ajout."""
    NOM = input("Nom du produit à vérifier : ")
    if NOM in Stock and NOM in Seuils:
        if Stock[NOM] <= Seuils[NOM]:
            print(f"ALERTE : Le produit {NOM} a un stock faible ({Stock[NOM]}).")
        else:
            print(f"Le stock de {NOM} est suffisant ({Stock[NOM]}).")
    else:
        print("Produit introuvable ou seuil non défini.")

###
def trier_produit_prix():
    """Crée une liste temporaire de tuples (prix, nom) pour utiliser sort()."""
    liste_a_trier = []
    for nom, val in Produit.items():
        prix = val[0]
        liste_a_trier.append((prix, nom))

    liste_a_trier.sort() # Trie par défaut sur le premier élément (le prix)

    print("--- Liste par PRIX (Croissant) ---")
    for prix, nom in liste_a_trier:
        print(f"{nom} : {prix} MAD")

###
def trier_produit_Categorie():
    """Similaire au tri par prix, mais place la catégorie en premier élément de tri."""
    liste_a_trier = []
    for nom, val in Produit.items():
        categ = val[1]
        liste_a_trier.append((categ, nom))

    liste_a_trier.sort()

    print("--- Liste par Catégorie ---")
    for categ, nom in liste_a_trier:
        print(f"{nom} : {categ}")

###
def calculer_valeur_total_stock():
    """Parcourt l'inventaire pour faire la somme (Prix * Quantité)."""
    total = 0
    for nom in Produit:
        prix = Produit[nom][0]
        qte = Stock[nom]
        total += prix * qte
    print(f"Valeur totale de l'inventaire : {total} MAD")

###
def recherch_P_N():
    """Moteur de recherche par clé directe dans le dictionnaire."""
    produit_search = input("Nom du produit à rechercher : ")
    if produit_search in Produit:
        prix, categorie = Produit[produit_search]
        quantite = Stock[produit_search]

        return (f"PRODUIT : {produit_search}\n"
                f"PRIX : {prix} MAD | CATEGORIE : {categorie}\n"
                f"STOCK : {quantite}")
    else:
        return f"Le produit '{produit_search}' n'est pas dans l'inventaire. Merci de l'ajouter !"

###
def afficher_inventaire_complet():
    """Affiche un tableau formaté avec alignement des colonnes."""
    print(f"\n{'NOM':<15} | {'PRIX':<10} | {'CATÉGORIE':<15} | {'STOCK':<5}")
    print("-" * 55)
    for nom in Produit:
        prix, cat = Produit[nom]
        qte = Stock[nom]
        # <15 signifie 15 caractères d'espace, aligné à gauche
        print(f"{nom:<15} | {prix:<10.2f} | {cat:<15} | {qte:<5}")

###
def sauvgard_donner():
    """Crée un dossier dans 'Documents' et exporte les dictionnaires en CSV."""
    dossier_documents = os.path.join(os.path.expanduser("~"), "Documents")
    dossier_save = os.path.join(dossier_documents, "S_G_I_SAVE")

    # Création du dossier si inexistant
    if not os.path.exists(dossier_save):
        os.makedirs(dossier_save)
        print(f"Dossier créé : {dossier_save}")

    # Génération du nom de fichier avec la date du jour
    date_str = datetime.now().strftime("%d-%m-%Y")
    nom_fichier = f"SAUVGARD_DU_{date_str}.csv"
    chemin_complet = os.path.join(dossier_save, nom_fichier)

    try:
        with open(chemin_complet, mode="w", newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['NOM', 'PRIX', 'CATEGORIE', 'STOCK', 'SEUIL']) # En-tête
            for nom in Produit:
                prix, cat = Produit[nom]
                qte = Stock.get(nom, 0)
                limite = Seuils.get(nom, 0)
                writer.writerow([nom, prix, cat, qte, limite])
                
        print(f"Sauvegarde réussie dans : {chemin_complet}")
    except Exception as e:
        print(f"Erreur lors de l'écriture : {e}")

###
def importer_sauvegarde_csv():
    """Lit un fichier CSV pour remplir les dictionnaires du programme."""
    home = os.path.expanduser("~")
    dossier_save = os.path.join(home, "Documents", "S_G_I_SAVE")
    
    nom_fichier = input("Nom du fichier à charger (ex: SAUVGARD_DU_08-03-2026.csv) : ")
    chemin_complet = os.path.join(dossier_save, nom_fichier)

    if not os.path.exists(chemin_complet):
        print(f"Erreur : Le fichier {nom_fichier} est introuvable.")
        return

    try:
        with open(chemin_complet, mode="r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader) # Saute la ligne d'en-tête

            # On vide l'inventaire actuel avant d'importer
            Produit.clear()
            Stock.clear()
            Seuils.clear()

            for ligne in reader:
                nom = ligne[0]
                Produit[nom] = (float(ligne[1]), ligne[2]) 
                Stock[nom] = int(ligne[3])                 
                Seuils[nom] = int(ligne[4])                
                
        print(f"Données chargées avec succès depuis {nom_fichier} !")
    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")

###       
def menu():
    """Boucle principale de l'interface utilisateur."""
    while True:
        print("\n--- GESTION D'INVENTAIRE ---")
        print("1. Ajouter un produit")
        print("2. Supprimer un produit")
        print("3. Modifier un produit")
        print("4. Vérifier stock faible")
        print("5. Trier par prix")
        print("6. Trier par catégorie")
        print("7. Calculer valeur totale")
        print("8. Rechercher un produit")
        print("9. Afficher tout l'inventaire")
        print("10. Sauvegarder l'inventaire (CSV)")
        print("11. Importer une sauvegarde (CSV)")
        print("12. Quitter")
        
        choix = input("\nChoisissez une option (1-12) : ")

        if choix == "1":
            ajouter_produit_stock()
        elif choix == "2":
            supprime_produit_stock()
        elif choix == "3":
            modifer_produit_stock()
        elif choix == "4":
            verifier_stock()
        elif choix == "5":
            trier_produit_prix()
        elif choix == "6":
            trier_produit_Categorie()
        elif choix == "7":
            calculer_valeur_total_stock()
        elif choix == "8":
            print(recherch_P_N())
        elif choix == "9":
            afficher_inventaire_complet()
        elif choix == "10":
            sauvgard_donner()
        elif choix == "11":
            importer_sauvegarde_csv()
        elif choix == "12":
            print("Au revoir !")
            break
        else:
            print("Option invalide, réessayez.")

# --- POINT D'ENTRÉE DU PROGRAMME ---
if __name__ == "__main__":
    menu()