 Ce projet, intitulé **Système de Gestion d’Inventaire (S_G_I)**, est une application console développée en **Python** permettant de gérer efficacement le stock de produits pour une entreprise ou un commerce.

Voici une description détaillée des composants et fonctionnalités de votre projet :

---

## 🛠️ Architecture des Données

Le programme utilise une approche de **base de données locale** basée sur trois dictionnaires synchronisés par le nom du produit (clé unique) :

*  : Gère les informations descriptives (Prix, Catégorie).
*  : Suit les quantités physiques disponibles.
*  : Enregistre les limites d'alerte pour le réapprovisionnement.

## 🚀 Fonctionnalités Principales

L'application offre un cycle de gestion complet (CRUD) ainsi que des outils d'analyse :

### 1. Gestion du Stock (Opérations de base)

* **Ajout/Modification/Suppression** : Permet de créer de nouveaux articles, de mettre à jour les prix/quantités ou de retirer des produits de l'inventaire.
* **Recherche Intuitive** : Un moteur de recherche par nom pour consulter instantanément les détails d'un produit spécifique.

### 2. Analyse et Surveillance

* **Alerte de Stock Faible** : Compare automatiquement les quantités en main avec les seuils définis pour prévenir les ruptures de stock.
* **Calcul de Valeur** : Calcule dynamiquement la valeur financière totale de l'inventaire (Prix $\times$ Quantité).
* **Tri Avancé** : Visualisation organisée des produits par ordre de prix croissant ou par catégorie.

### 3. Persistance des Données (Sauvegarde)

* **Export CSV** : Sauvegarde l'intégralité des données dans un dossier dédié () avec un horodatage automatique.
* **Importation** : Permet de restaurer une session de travail précédente en chargeant un fichier CSV existant.

## 💻 Interface Utilisateur

Le projet utilise un **menu interactif numéroté (1 à 12)** pour une navigation simple en ligne de commande. L'affichage de l'inventaire complet est formaté sous forme de tableau pour une lecture claire et professionnelle.

---

**Souhaitez-vous que je rédige un fichier  professionnel pour votre dépôt GitHub basé sur ces éléments ?**
Ce projet, intitulé Système de Gestion d’Inventaire (S_G_I), est une application console développée en Python permettant de gérer efficacement le stock de produits pour une entreprise ou un commerce.
