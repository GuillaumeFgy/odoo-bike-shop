MAGASIN DE VELOS - Odoo 19.0
============================

Projet de gestion d'un magasin de vélos avec location et vente.


INSTALLATION
------------

1. Lancer avec Docker :
   docker-compose up -d

2. Accès :
   http://localhost:8069
   Base : bike_shop / admin / admin

3. Installer les modules :
   Apps > Rechercher "Bike Shop" > Installer


MODULES
-------

MODULE LOCATION (bike_shop_rental) :
- Gestion des vélos de location par catégories (Ville, VTT, Route, Électrique, Enfant)
- Contrats de location avec tarification flexible (horaire/journalier/hebdomadaire/mensuel)
- Workflow complet : Brouillon > Confirmé > En cours > Terminé > Facturé > Payé
- Suivi de disponibilité des vélos en temps réel
- Validation des données client (email, téléphone, nom)
- Contraintes métier (durées minimales selon type de location)
- Rapports d'analyse des locations et taux d'occupation
- Impression de contrats PDF

MODULE VENTE (bike_shop_sale) :
- Catalogue de produits (vélos, accessoires, pièces)
- Calcul automatique de la marge (montant en € et pourcentage)
- Commandes clients avec lignes de commande
- Gestion automatique du stock (déduction à la confirmation)
- Workflow : Brouillon > Confirmé > Facturé > Payé > Terminé
- Validation des données et vérification du stock disponible
- Suppression sécurisée des produits (protection si utilisés dans commandes actives)
- Vue Kanban pour suivi visuel des commandes


FONCTIONNALITES PRINCIPALES
---------------------------

LOCATION :
- Sélection de vélo parmi les vélos disponibles uniquement
- Calcul automatique des durées et tarifs
- Validation des dates (pas de début dans le passé, fin après début)
- Vérification de cohérence durée/type de location
- Changement d'état du vélo lors du démarrage/retour
- Gestion des annulations (uniquement avant démarrage)

VENTE :
- Création de commandes multi-produits
- Vérification du stock avant confirmation
- Déduction automatique du stock à la confirmation
- Remise en stock lors de l'annulation
- Impossibilité d'annuler une commande facturée

VALIDATIONS :
- Format email : exemple@domaine.com
- Format téléphone : minimum 10 chiffres (accepte +33, espaces, tirets)
- Nom client : minimum 2 caractères, sans chiffres
- Quantités positives
- Prix positifs
- Prix de vente supérieur ou égal au prix d'achat (marge positive)


UTILISATION
-----------

LOCATION :
1. Bike Shop > Location > Contrats > Nouveau
2. Saisir client (existant ou nouveau) + coordonnées
3. Sélectionner vélo disponible + dates + type de tarification
4. Confirmer le contrat (vérifie disponibilité)
5. Démarrer la location (vélo passe en "Loué")
6. Terminer la location (vélo redevient disponible)
7. Facturer puis Marquer comme payé

VENTE :
Gestion des produits :
1. Bike Shop > Vente > Produits > Nouveau
2. Saisir nom, type, prix de vente et prix d'achat
3. La marge (€ et %) est calculée automatiquement
4. Confirmer le produit
5. Les produits peuvent être supprimés s'ils ne sont pas utilisés dans des commandes actives

Gestion des commandes :
1. Bike Shop > Vente > Commandes > Nouveau
2. Saisir client + coordonnées
3. Ajouter lignes de produits (quantités, prix auto-rempli)
4. Confirmer (vérifie et déduit le stock)
5. Facturer puis Marquer comme payé
6. Marquer comme terminé

RAPPORTS :
- Bike Shop > Location > Rapports
- Analyse des locations par période
- Taux d'occupation par vélo/catégorie


DONNEES DEMO
------------

- Partenaires de démonstration
- 6 vélos de location avec tarifs configurés
- Exemples de contrats de location
- Produits à vendre (vélos, accessoires, pièces)
- Exemples de commandes de vente


STRUCTURE TECHNIQUE
-------------------

custom_addons/
├── bike_shop_rental/
│   ├── models/
│   │   ├── bike.py (modèle Bike avec états et tarifs)
│   │   ├── bike_category.py (catégories de vélos)
│   │   ├── rental_order.py (contrats de location)
│   │   └── rental_report.py (rapports d'analyse)
│   ├── views/
│   │   ├── bike_views.xml
│   │   ├── rental_order_views.xml
│   │   └── reports/
│   └── data/ (catégories et données de démo)
│
└── bike_shop_sale/
    ├── models/
    │   ├── product.py (modèle ShopProduct personnalisé)
    │   └── sale_order.py (modèle ShopOrder + ShopOrderLine)
    └── views/
        ├── product_views.xml
        └── sale_order_views.xml
