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


FONCTIONNALITES
---------------

LOCATION :
- Vélos par catégories (Ville, VTT, Route, Électrique, Enfant)
- Contrats avec tarification (heure/jour/semaine/mois)
- Suivi de disponibilité
- Facturation

VENTE :
- Produits : vélos, accessoires, pièces
- Commandes clients
- Gestion du stock

RAPPORTS :
- Analyse des locations
- Taux d'occupation des vélos


UTILISATION
-----------

Location :
  Bike Shop > Location > Contrats
  Nouveau > Client + Vélo + Dates > Confirmer > Démarrer > Terminer > Facturer

Vente :
  Bike Shop > Vente > Commandes
  Nouveau > Client + Produits > Confirmer


DONNEES DEMO
------------

- 3 clients
- 6 vélos de location
- 3 contrats (en cours, confirmé, terminé)
- 5 produits à vendre
- 1 commande de vente
