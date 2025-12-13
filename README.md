Test# 🚴 Bike Shop - Système de Gestion Odoo

[![Odoo Version](https://img.shields.io/badge/Odoo-19.0-blue)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-green)](https://www.gnu.org/licenses/lgpl-3.0.html)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://www.python.org/)

Système complet de gestion pour un magasin de vélos basé sur Odoo 19.0 Community Edition.

## 📋 Table des Matières

- [Contexte du Projet](#contexte-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
  - [Option 1: Installation avec Docker (Recommandé)](#option-1-installation-avec-docker-recommandé)
  - [Option 2: Installation Manuelle](#option-2-installation-manuelle)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Démonstration](#démonstration)
- [Rapports et Analyses](#rapports-et-analyses)
- [Structure du Projet](#structure-du-projet)
- [Développement](#développement)
- [Déploiement](#déploiement)
- [FAQ](#faq)
- [Support](#support)
- [Auteurs](#auteurs)
- [Licence](#licence)

## 🎯 Contexte du Projet

Ce projet a été développé dans le cadre d'un examen académique pour démontrer la mise en place d'un système ERP complet avec Odoo 19.0 Community Edition pour un magasin de vélos.

**Objectifs:**
- Gérer la vente de vélos, accessoires et pièces détachées
- Gérer la location de vélos (courte et longue durée)
- Suivre le stock et les clients
- Générer des rapports de performance

**Contraintes:**
- Odoo 19.0 Community Edition (gratuit, sans licence payante)
- Code source public sur GitHub
- Démonstration locale (pas d'hébergement cloud requis)
- Modules personnalisés suivant les conventions Odoo

## ✨ Fonctionnalités

### 🏪 Vente
- ✅ Catalogue de produits (vélos, accessoires, pièces détachées)
- ✅ Gestion des commandes clients
- ✅ Facturation automatique
- ✅ Gestion du stock (entrées/sorties)
- ✅ Historique des ventes par client
- ✅ Reporting des ventes par produit et catégorie

### 🚲 Location
- ✅ Gestion des vélos disponibles à la location
- ✅ Contrats de location (horaire, journalier, hebdomadaire, mensuel)
- ✅ Tarification flexible et automatique
- ✅ Suivi de la disponibilité en temps réel
- ✅ Calendrier des locations
- ✅ Gestion des cautions
- ✅ Rapport de taux d'occupation

### 👥 Clients
- ✅ Fiches clients complètes
- ✅ Historique des achats
- ✅ Historique des locations
- ✅ Coordonnées et informations de contact

### 📊 Reporting
- ✅ Analyse des ventes (pivot, graphiques)
- ✅ Taux d'occupation des vélos
- ✅ Revenus par catégorie
- ✅ Statistiques de location
- ✅ Export PDF des contrats

## 🏗️ Architecture

### Modules Personnalisés

Le projet comprend **2 modules personnalisés** :

#### 1. **bike_shop_rental** - Module de Location
Module principal pour la gestion des locations de vélos.

**Modèles:**
- `bike.category` - Catégories de vélos (VTT, Route, Ville, Électrique, etc.)
- `bike.bike` - Vélos individuels avec caractéristiques et état
- `rental.order` - Contrats de location
- `rental.report` - Vues d'analyse des locations
- `bike.occupancy.report` - Rapport de taux d'occupation

**Fonctionnalités clés:**
- Gestion complète du cycle de vie d'une location
- Calcul automatique des tarifs selon la durée
- Vérification de disponibilité automatique
- Génération de contrats PDF
- Statistiques en temps réel

#### 2. **bike_shop_sale** - Module de Vente Étendu
Extension du module de vente standard Odoo pour les vélos.

**Fonctionnalités:**
- Champs personnalisés pour les vélos (marque, modèle, taille, etc.)
- Support des vélos électriques (batterie, autonomie, vitesse)
- Gestion des accessoires et pièces détachées
- Garantie personnalisée par produit
- Intégration avec le stock

### Modules Odoo Standard Utilisés
- `sale_management` - Gestion des ventes
- `stock` - Gestion du stock
- `product` - Gestion des produits
- `account` - Comptabilité et facturation

## 💻 Prérequis

### Option Docker (Recommandé)
- Docker Desktop ou Docker Engine (v20.10+)
- Docker Compose (v2.0+)
- 4 GB RAM minimum
- 10 GB espace disque

### Option Installation Manuelle
- Python 3.10+
- PostgreSQL 13+
- Node.js 16+ (optionnel, pour les assets)
- Dépendances système (voir section Installation Manuelle)

## 🚀 Installation

### Option 1: Installation avec Docker (Recommandé)

C'est la méthode la plus simple et rapide pour démarrer.

#### Étape 1: Cloner le repository

```bash
git clone https://github.com/MattLambot/odoo-bike-shop.git
cd odoo-bike-shop
```

#### Étape 2: Démarrer les containers

```bash
docker-compose up -d
```

Cette commande va:
- Télécharger l'image Odoo 19.0
- Créer une base de données PostgreSQL
- Monter les modules personnalisés
- Démarrer Odoo sur http://localhost:8069

#### Étape 3: Créer la base de données

1. Ouvrez votre navigateur sur http://localhost:8069
2. Créez une nouvelle base de données:
   - **Database Name:** `bike_shop`
   - **Email:** votre email
   - **Password:** votre mot de passe admin
   - **Language:** French / Français
   - **Country:** France
   - **Demo data:** ✅ Cochez pour avoir les données de démonstration

#### Étape 4: Installer les modules

Une fois connecté à Odoo:

1. Allez dans **Apps** (Applications)
2. Recherchez "Bike Shop"
3. Installez les modules dans cet ordre:
   - **Bike Shop - Rental Management** (installe automatiquement les dépendances)
   - **Bike Shop - Sales Management**

**Temps d'installation:** ~2-3 minutes

#### Étape 5: Vérification

Après installation, vous devriez voir:
- Un menu "Bike Shop" dans la barre de navigation
- Des sous-menus: Location, Vente, Stock, Rapports, Configuration
- Des données de démonstration (vélos, clients, contrats)

### Option 2: Installation Manuelle

#### Prérequis système (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3-pip python3-dev libxml2-dev libxslt1-dev \
    libldap2-dev libsasl2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
    zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
    libfribidi-dev libxcb1-dev postgresql postgresql-client
```

#### Étape 1: Cloner et installer Odoo

```bash
# Cloner le projet
git clone https://github.com/MattLambot/odoo-bike-shop.git
cd odoo-bike-shop

# Cloner Odoo 19.0
git clone --depth 1 --branch 19.0 https://github.com/odoo/odoo.git

# Installer les dépendances Python
pip3 install -r odoo/requirements.txt
```

#### Étape 2: Configurer PostgreSQL

```bash
# Créer un utilisateur PostgreSQL
sudo -u postgres createuser -s $USER

# Créer la base de données
createdb bike_shop
```

#### Étape 3: Configurer Odoo

Éditez le fichier `odoo.conf` et ajustez les chemins:

```ini
[options]
addons_path = /chemin/vers/odoo-bike-shop/custom_addons,/chemin/vers/odoo/addons
db_host = localhost
db_port = 5432
db_user = votre_utilisateur
db_password = votre_mot_de_passe
```

#### Étape 4: Démarrer Odoo

```bash
./odoo/odoo-bin -c odoo.conf -d bike_shop -i base --without-demo=False
```

#### Étape 5: Installer les modules

Suivez les mêmes étapes que pour Docker (Étape 4-5)

## ⚙️ Configuration

### Configuration de Base

Après installation, configurez:

1. **Entreprise** (Settings > Companies)
   - Nom: Bike Shop
   - Adresse, téléphone, email
   - Logo

2. **Utilisateurs** (Settings > Users)
   - Créez des utilisateurs pour les vendeurs
   - Assignez les droits: Sales / User ou Sales / Manager

3. **Catégories de Vélos** (Bike Shop > Configuration > Catégories de Vélos)
   - Vérifiez/modifiez les catégories existantes
   - Ajustez les tarifs par défaut

4. **Produits** (Bike Shop > Vente > Vélos à Vendre)
   - Vérifiez les produits de démonstration
   - Ajoutez vos propres produits

### Configuration Avancée

#### Configurer les Taxes

Settings > Accounting > Taxes
- TVA 20% pour la France
- TVA réduite 5.5% si applicable

#### Configurer les Méthodes de Paiement

Settings > Accounting > Payment Methods
- Espèces
- Carte bancaire
- Virement

#### Configurer les Entrepôts

Inventory > Configuration > Warehouses
- Définissez votre entrepôt principal
- Configurez les emplacements de stock

## 📖 Utilisation

### Créer une Location

1. **Bike Shop > Location > Contrats de Location**
2. Cliquez sur **Créer**
3. Remplissez:
   - Client (créez-le si nécessaire)
   - Vélo (seuls les vélos disponibles sont affichés)
   - Date de début et fin
   - Type de location (horaire/journalier/hebdomadaire/mensuel)
4. Le système calcule automatiquement:
   - La durée
   - Le tarif selon le type de location
   - Le total avec caution
5. **Confirmer** le contrat
6. **Démarrer** la location quand le client récupère le vélo
7. **Terminer** la location au retour du vélo
8. **Créer une facture** si nécessaire

### Créer une Vente

1. **Bike Shop > Vente > Commandes de Vente**
2. Cliquez sur **Créer**
3. Sélectionnez le client
4. Ajoutez des produits:
   - Vélos
   - Accessoires
   - Pièces détachées
5. **Confirmer** la commande
6. **Créer une facture**
7. Enregistrer le paiement

### Gérer le Stock

1. **Bike Shop > Stock**
2. Réceptions: Enregistrez les nouvelles arrivées
3. Livraisons: Préparez et validez les livraisons clients
4. Ajustements: Corrigez les quantités en stock

### Consulter les Rapports

#### Rapport de Locations
**Bike Shop > Rapports > Analyse des Locations**
- Vue graphique: Revenus par catégorie
- Vue pivot: Analyse multidimensionnelle
- Filtres: Période, état, type de location

#### Taux d'Occupation
**Bike Shop > Rapports > Taux d'Occupation**
- Nombre de locations par vélo
- Jours totaux loués
- Revenus par vélo
- Durée moyenne de location

#### Rapport de Ventes
**Bike Shop > Vente > Commandes de Vente > Reporting**
- Analyse des ventes par produit
- Graphiques et tableaux croisés dynamiques

## 🎬 Démonstration

Le projet inclut des données de démonstration pour tester rapidement.

### Données Incluses

**Clients** (3):
- Jean Dupont (Paris)
- Marie Martin (Lyon)
- Pierre Durant (Marseille)

**Vélos** (6):
- TREK City 2023
- SPECIALIZED Mountain X5
- GIANT Road Pro
- BOSCH E-Bike Urban
- DECATHLON Kids 20"
- TREK Mountain Pro (actuellement loué)

**Produits à Vendre** (12+):
- 4 vélos neufs
- 4 accessoires (casque, antivol, éclairage, pompe)
- 4 pièces détachées (pneus, chambres à air, chaîne, freins)

**Contrats de Location** (3):
- 1 en cours
- 1 confirmé (futur)
- 1 terminé

**Commandes de Vente** (1):
- 1 commande confirmée avec vélo + accessoires

### Scénario de Test Complet

1. **Consulter le tableau de bord**
   - Vérifiez les vélos disponibles
   - Consultez le planning des locations

2. **Créer une nouvelle location**
   - Client: Marie Martin
   - Vélo: GIANT Road Pro
   - Dates: Aujourd'hui + 3 jours
   - Type: Journalier
   - Confirmez et démarrez

3. **Créer une vente**
   - Client: Jean Dupont
   - Produits: Casque + Antivol
   - Confirmez et facturez

4. **Consulter les rapports**
   - Analyse des locations
   - Taux d'occupation
   - Ventes

## 📊 Rapports et Analyses

### Rapports Disponibles

| Rapport | Description | Vues |
|---------|-------------|------|
| **Analyse des Locations** | Revenus et statistiques de location | Graph, Pivot, Tree |
| **Taux d'Occupation** | Performance par vélo | Tree, Graph |
| **Contrat de Location PDF** | Document contractuel | PDF |
| **Analyse des Ventes** | Performance commerciale | Graph, Pivot |

### Export de Données

Tous les rapports peuvent être exportés en:
- **Excel/CSV** - Pour analyse externe
- **PDF** - Pour impression

## 📁 Structure du Projet

```
odoo-bike-shop/
├── custom_addons/                 # Modules personnalisés
│   ├── bike_shop_rental/          # Module de location
│   │   ├── models/                # Modèles Python
│   │   │   ├── bike.py
│   │   │   ├── bike_category.py
│   │   │   ├── rental_order.py
│   │   │   └── rental_report.py
│   │   ├── views/                 # Vues XML
│   │   │   ├── bike_views.xml
│   │   │   ├── rental_order_views.xml
│   │   │   ├── menu_views.xml
│   │   │   └── reports/
│   │   ├── security/              # Droits d'accès
│   │   ├── data/                  # Données initiales
│   │   ├── reports/               # Rapports PDF
│   │   └── __manifest__.py
│   │
│   └── bike_shop_sale/            # Module de vente
│       ├── models/
│       │   ├── product_template.py
│       │   └── sale_order.py
│       ├── views/
│       ├── security/
│       ├── data/
│       └── __manifest__.py
│
├── docker-compose.yml             # Configuration Docker
├── odoo.conf                      # Configuration Odoo
├── README.md                      # Ce fichier
└── .gitignore
```

## 🛠️ Développement

### Ajouter un Nouveau Champ

Exemple: Ajouter un champ "Numéro de chassis" au vélo

1. Modifiez `custom_addons/bike_shop_rental/models/bike.py`:

```python
chassis_number = fields.Char(string='Numéro de Chassis')
```

2. Ajoutez le champ dans la vue `bike_views.xml`:

```xml
<field name="chassis_number"/>
```

3. Mettez à jour le module:
   - Apps > Bike Shop - Rental Management
   - Upgrade

### Créer un Nouveau Rapport

Voir les exemples dans `bike_shop_rental/reports/`

### Bonnes Pratiques

- Suivez les conventions de nommage Odoo
- Commentez votre code
- Testez avant de commiter
- Utilisez les traductions pour le multilingue

## 🌐 Déploiement

### Déploiement Local

Le mode Docker Compose est parfait pour une démonstration locale.

**Avantages:**
- ✅ Rapide à mettre en place
- ✅ Isolé du système
- ✅ Facile à supprimer

**Limites:**
- ❌ Pas accessible depuis l'extérieur
- ❌ Données perdues si container supprimé (utiliser volumes)
- ❌ Pas de HTTPS

### Déploiement Production (Options)

#### Option 1: Serveur VPS (Ubuntu)
- Serveur: OVH, DigitalOcean, AWS EC2, etc.
- Coût: 5-20€/mois
- Nécessite: Configuration nginx, SSL, backup

#### Option 2: Odoo.sh
- Solution cloud officielle Odoo
- Coût: À partir de 17€/mois/utilisateur
- ⚠️ Version Enterprise uniquement

#### Option 3: Kubernetes
- Pour grande échelle
- Nécessite expertise DevOps

### Sauvegardes

#### Backup Base de Données

```bash
# Avec Docker
docker-compose exec db pg_dump -U odoo bike_shop > backup.sql

# Manuel
pg_dump bike_shop > backup.sql
```

#### Backup Filestore

```bash
# Docker
docker cp odoo_bike_shop:/var/lib/odoo ./backup-filestore

# Manuel
cp -r ~/.local/share/Odoo/filestore/bike_shop ./backup-filestore
```

## ❓ FAQ

### Odoo ne démarre pas

**Problème:** `ImportError: No module named 'xxx'`

**Solution:**
```bash
pip3 install -r odoo/requirements.txt
```

### Les modules n'apparaissent pas

**Solution:**
1. Vérifiez que `addons_path` est correct dans `odoo.conf`
2. Redémarrez Odoo
3. Apps > Update Apps List

### Erreur de base de données

**Problème:** `FATAL: password authentication failed`

**Solution:**
Vérifiez les credentials PostgreSQL dans `odoo.conf` ou `docker-compose.yml`

### Le port 8069 est déjà utilisé

**Solution:**
Modifiez le port dans `docker-compose.yml`:
```yaml
ports:
  - "8070:8069"
```

Puis accédez via http://localhost:8070

### Comment réinitialiser les données ?

**Docker:**
```bash
docker-compose down -v
docker-compose up -d
```

**Manuel:**
```bash
dropdb bike_shop
createdb bike_shop
./odoo/odoo-bin -c odoo.conf -d bike_shop -i base --without-demo=False
```

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/MattLambot/odoo-bike-shop/issues)
- **Documentation Odoo:** [odoo.com/documentation/19.0](https://www.odoo.com/documentation/19.0)
- **Forum Odoo:** [odoo.com/forum](https://www.odoo.com/forum)

## 👥 Auteurs

**Bike Shop Team**
- Projet académique - Odoo 19.0
- 2024-2025

## 📄 Licence

Ce projet est sous licence **LGPL-3.0**.

Les modules Odoo doivent être sous licence LGPL-3.0 ou compatibles.

---

## 🎯 Checklist de Présentation

Pour la soutenance du projet:

- [ ] Démonstration de l'installation (Docker)
- [ ] Présentation des modules personnalisés
- [ ] Démonstration: Créer une location
- [ ] Démonstration: Créer une vente
- [ ] Démonstration: Consulter les rapports
- [ ] Explication de l'architecture technique
- [ ] Discussion sur les choix de conception
- [ ] Questions/Réponses

**Bonne présentation ! 🚴‍♂️**
