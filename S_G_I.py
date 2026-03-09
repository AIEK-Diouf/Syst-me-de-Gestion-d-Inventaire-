import os
import csv
from datetime import datetime

Produit = {}
Stock = {}
Seuils = {}



###
def ajouter_produit_stock():
    NOM = input("Nom du produit : ")
    PRIX = float(input("Prix du produit en MAD : "))
    CAT = input("Catégorie du produit : ")
    QTE = int(input("Stock du produit : "))
    LIMITE = int(input("Seuil d'alerte : "))


    Produit[NOM] = (PRIX, CAT)
    Stock[NOM] = QTE
    Seuils[NOM] = LIMITE

    print(f"Le produit {NOM} a été ajouté avec succès.")

###
def supprime_produit_stock():
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
    NOM = input("Nom du produit à modifier : ")
    if NOM in Produit:
        PRIX = float(input("Nouveau prix : "))
        CAT = input("Nouvelle catégorie : ")
        QTE = int(input("Nouveau stock : "))

        Produit[NOM] = (PRIX, CAT)
        Stock[NOM] = QTE
        print(f"Le produit {NOM} a été modifié avec succès.")
    else:
        print("Le produit n'existe pas !")
        print("Ajoute le")

###
def verifier_stock():

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
    liste_a_trier = []
    for nom, val in Produit.items():
        prix = val[0]
        liste_a_trier.append((prix, nom))

    liste_a_trier.sort()

    print("--- Liste par PRIX (Croissant) ---")
    for prix, nom in liste_a_trier:
        print(f"{nom} : {prix} MAD")

###
def trier_produit_Categorie():
    liste_a_trier = []
    for nom, val in Produit.items():
        categ = val[1]
        # On met la catégorie en premier
        liste_a_trier.append((categ, nom))

    liste_a_trier.sort()

    print("--- Liste par Catégorie ---")
    for categ, nom in liste_a_trier:
        print(f"{nom} : {categ}")


###
def calculer_valeur_total_stock():
    total = 0
    for nom in Produit:
        prix = Produit[nom][0]
        qte = Stock[nom]
        total += prix * qte
    print(f"Valeur totale de l'inventaire : {total} MAD")


###
def recherch_P_N():
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
    print(f"\n{'NOM':<15} | {'PRIX':<10} | {'CATÉGORIE':<15} | {'STOCK':<5}")
    print("-" * 55)
    for nom in Produit:
        prix, cat = Produit[nom]
        qte = Stock[nom]

        print(f"{nom:<15} | {prix:<10.2f} | {cat:<15} | {qte:<5}")
###
def sauvgard_donner():
    dossier_documents = os.path.join(os.path.expanduser("~"), "Documents")
    dossier_save = os.path.join(dossier_documents, "S_G_I_SAVE")

    if not os.path.exists(dossier_save):
        os.makedirs(dossier_save)
        print(f"Dossier créé : {dossier_save}")

    date_str = datetime.now().strftime("%d-%m-%Y")
    nom_fichier = f"SAUVGARD_DU_{date_str}.csv"
    chemin_complet = os.path.join(dossier_save, nom_fichier)

    try:
        with open(chemin_complet, mode="w", newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=',')
            
            writer.writerow(['NOM', 'PRIX', 'CATEGORIE', 'STOCK', 'SEUIL'])
            for nom in Produit:
                prix, cat = Produit[nom]
                qte = Stock.get(nom, 0)
                limite = Seuils.get(nom, 0)
                writer.writerow([nom, prix, cat, qte, limite])
                
        print(f"Sauvegarde réussie dans : {chemin_complet}")
    except Exception as e:
        print(f"Erreur : {e}")
###
def importer_sauvegarde_csv():
    home = os.path.expanduser("~")
    dossier_save = os.path.join(home, "Documents", "S_G_I_SAVE")
    
    nom_fichier = input("Nom du fichier à charger (ex: SAUVGARD_DU_08-03-2026.csv) : ")
    chemin_complet = os.path.join(dossier_save, nom_fichier)

    if not os.path.exists(chemin_complet):
        print(f"Erreur : Le fichier {nom_fichier} est introuvable dans {dossier_save}")
        return

    try:
        with open(chemin_complet, mode="r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)  

            
            Produit.clear()
            Stock.clear()
            Seuils.clear()

            for ligne in reader:
                nom = ligne[0]
                Produit[nom] = (float(ligne[1]), ligne[2]) 
                Stock[nom] = int(ligne[3])                 
                Seuils[nom] = int(ligne[4])                
                
        print(f" Données chargées avec succès depuis {nom_fichier} !")
    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")
###       
def menu():

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
        if choix == "10":
            sauvgard_donner()
        elif choix == "11":
            importer_sauvegarde_csv()
        elif choix == "12":
            print("Au revoir !")
            break
        else:
            print("Option invalide, réessayez.")



if __name__ == "__main__":
    menu()
