'''
Moteur de Gestion d'Inventaire (Back-end)
'''
import csv
import os
import re

Produit = {}  
Stock = {}    
Seuils = {}   


def ajouter_modifier_produit(nom, prix, cat, qte, limite):
    """
    Extrait les chiffres des entrées pour éviter les erreurs de format (comme 'MAD' ou 'OK').
    """
    try:
        n = str(nom).lower().strip()
        
        # On extrait uniquement les chiffres et le point pour le prix
        p_clean = "".join(re.findall(r"[\d\.]+", str(prix).replace(',', '.')))
        p_val = float(p_clean)
        
        # On extrait uniquement les chiffres pour le stock et le seuil
        q_clean = "".join(re.findall(r"\d+", str(qte)))
        s_clean = "".join(re.findall(r"\d+", str(limite)))
        
        Produit[n] = (p_val, str(cat).lower().strip())
        Stock[n] = int(q_clean)
        Seuils[n] = int(s_clean)
        return True
    except (ValueError, IndexError):
        return False
    
def supprimer_produit(nom):
    """Retire un produit des dictionnaires."""
    n = nom.lower().strip()
    if n in Produit:
        del Produit[n]
        del Stock[n]
        if n in Seuils: del Seuils[n]
        return True
    return False

def calculer_valeur_totale():
    """Calcule la somme totale (Prix * Quantité)."""
    total = 0
    for nom in Produit:
        total += Produit[nom][0] * Stock.get(nom, 0)
    return total

def sauvgard_donner(chemin_complet):
    """Enregistre les données dans un fichier CSV."""
    try:
        with open(chemin_complet, mode="w", newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['NOM', 'PRIX', 'CATEGORIE', 'STOCK', 'SEUIL'])
            for nom in Produit:
                prix, cat = Produit[nom]
                writer.writerow([nom, prix, cat, Stock.get(nom, 0), Seuils.get(nom, 0)])
        return True
    except Exception:
        return False

def importer_donner(chemin_complet):
    """Charge les données depuis un CSV et vide l'inventaire actuel."""
    try:
        with open(chemin_complet, mode="r", newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)
            Produit.clear()
            Stock.clear()
            Seuils.clear()
            for ligne in reader:
                if len(ligne) == 5:
                    nom = ligne[0].lower().strip()
                    Produit[nom] = (float(ligne[1]), ligne[2].strip())
                    Stock[nom] = int(ligne[3])
                    Seuils[nom] = int(ligne[4])
        return True
    except Exception:
        return False