# 🎤 Guide de Présentation - Bike Shop Odoo

Guide pour préparer et réussir votre présentation du projet devant le client/jury.

## 📅 Planning de Présentation

**Durée totale recommandée:** 10-15 minutes
- Introduction: 1-2 minutes
- Démonstration: 6-8 minutes
- Explication technique: 2-3 minutes
- Questions/Réponses: 2-3 minutes

---

## 1️⃣ Introduction (1-2 minutes)

### Ce qu'il faut dire

**Bonjour, nous sommes [Noms des membres du groupe].**

**Contexte du projet:**
"Nous avons développé un système complet de gestion pour un magasin de vélos en utilisant Odoo 19.0 Community Edition. Notre client souhaitait une solution gratuite, sans coûts de licence, pour gérer à la fois la vente et la location de vélos."

**Besoins identifiés:**
- Gérer un catalogue de produits (vélos, accessoires, pièces)
- Gérer les commandes et la facturation
- Gérer les locations courte et longue durée
- Suivre le stock en temps réel
- Générer des rapports de performance

**Notre solution:**
"Nous avons développé 2 modules personnalisés Odoo qui étendent les fonctionnalités standards pour répondre précisément aux besoins d'un magasin de vélos."

---

## 2️⃣ Démonstration Fonctionnelle (6-8 minutes)

### Préparation AVANT la présentation

1. **Odoo doit être démarré:**
   ```bash
   docker-compose up -d
   ```

2. **Ouvrez Odoo dans le navigateur:**
   - URL: http://localhost:8069
   - Connectez-vous AVANT la présentation

3. **Préparez plusieurs onglets:**
   - Onglet 1: Tableau de bord Bike Shop
   - Onglet 2: Liste des vélos
   - Onglet 3: Contrats de location (vide, prêt pour créer)
   - Onglet 4: Commandes de vente (vide, prêt pour créer)
   - Onglet 5: Rapports

### 2.1 Vue d'ensemble (30 secondes)

"Voici l'interface principale de notre système Bike Shop."

**Actions:**
1. Montrez le menu "Bike Shop" avec ses sous-menus
2. Expliquez la structure: Location, Vente, Stock, Rapports, Configuration

### 2.2 Démonstration Location (3 minutes)

**Étape 1: Montrer les vélos disponibles**

"Commençons par consulter notre parc de vélos disponibles à la location."

**Actions:**
1. Cliquez sur **Bike Shop > Location > Vélos**
2. Montrez la vue Kanban avec les photos
3. Sélectionnez un vélo et montrez ses caractéristiques:
   - Catégorie, marque, modèle
   - État (disponible, loué, maintenance)
   - Tarifs (horaire, journalier, hebdomadaire, mensuel)
   - Statistiques (nombre de locations, revenus)

**Phrase clé:**
"Chaque vélo a sa propre fiche avec toutes ses caractéristiques. Le système suit automatiquement son état et ses statistiques de location."

**Étape 2: Créer un contrat de location**

"Maintenant, créons un nouveau contrat de location."

**Actions:**
1. Allez dans **Bike Shop > Location > Contrats de Location**
2. Cliquez sur **Créer**
3. Remplissez le formulaire:
   - Client: Sélectionnez "Marie Martin"
   - Vélo: Sélectionnez "GIANT Road Pro" (montrez que seuls les vélos disponibles apparaissent)
   - Date début: Aujourd'hui
   - Date fin: Dans 3 jours
   - Type: Journalier

**Phrases clés:**
- "Le système vérifie automatiquement la disponibilité du vélo."
- "Les tarifs sont calculés automatiquement selon le type de location choisi."
- "La durée et le montant total (avec caution) sont calculés en temps réel."

4. Cliquez sur **Confirmer**
5. Montrez le changement d'état
6. Cliquez sur **Démarrer Location**

**Phrase clé:**
"Le vélo passe automatiquement en état 'Loué' et n'est plus disponible pour une autre location."

7. Montrez le **bouton Imprimer** pour générer le contrat PDF (optionnel)

### 2.3 Démonstration Vente (2 minutes)

"Passons maintenant à la partie vente."

**Actions:**
1. Allez dans **Bike Shop > Vente > Vélos à Vendre**
2. Montrez le catalogue de produits
3. Cliquez sur un vélo pour montrer les champs personnalisés:
   - Caractéristiques techniques (marque, modèle, taille, année)
   - Vélo électrique (batterie, autonomie)
   - Garantie

**Étape 2: Créer une commande de vente**

**Actions:**
1. Allez dans **Bike Shop > Vente > Commandes de Vente**
2. Créez une nouvelle commande:
   - Client: "Jean Dupont"
   - Ajoutez des produits:
     - 1x Casque Adulte
     - 1x Antivol U-Lock
3. Montrez le calcul automatique du total
4. Cliquez sur **Confirmer**

**Phrase clé:**
"La commande est confirmée et génère automatiquement les mouvements de stock et la facture."

### 2.4 Démonstration Rapports (1-2 minutes)

"Enfin, voyons les rapports de gestion."

**Actions:**
1. Allez dans **Bike Shop > Rapports > Analyse des Locations**
2. Montrez la **vue graphique** (revenus par catégorie)
3. Changez en **vue pivot** pour l'analyse multidimensionnelle
4. Allez dans **Taux d'Occupation**
5. Montrez les statistiques par vélo:
   - Nombre de locations
   - Total jours loués
   - Revenus générés

**Phrase clé:**
"Ces rapports permettent au gestionnaire d'analyser la performance de son parc de vélos et d'optimiser sa stratégie tarifaire."

---

## 3️⃣ Explication Technique (2-3 minutes)

### Architecture du système

**Slide ou explication verbale:**

"Notre solution repose sur une architecture modulaire:"

**Modules développés:**
1. **bike_shop_rental** - Module principal de location
   - 5 modèles Python (bike.category, bike.bike, rental.order, etc.)
   - Vues complètes (Kanban, Tree, Form, Calendar, Graph, Pivot)
   - Rapports PDF personnalisés
   - Calculs automatiques de tarification
   - Vérification de disponibilité en temps réel

2. **bike_shop_sale** - Extension des ventes
   - Extension du modèle produit standard Odoo
   - Champs spécifiques aux vélos
   - Support des vélos électriques
   - Intégration avec la gestion de stock

**Technologies:**
- Backend: Python 3.10 + Framework Odoo
- Base de données: PostgreSQL
- Frontend: XML (QWeb) + JavaScript
- Déploiement: Docker + Docker Compose

### Choix techniques justifiés

**Pourquoi Odoo Community ?**
- ✅ Gratuit (pas de coûts de licence)
- ✅ Framework mature et robuste
- ✅ Modules standards de qualité (ventes, stock, compta)
- ✅ Grande communauté de développeurs

**Pourquoi Docker ?**
- ✅ Installation simple et rapide
- ✅ Environnement reproductible
- ✅ Isolation du système
- ✅ Facilite le déploiement

**Pourquoi 2 modules distincts ?**
- ✅ Séparation des responsabilités (location vs vente)
- ✅ Maintenance facilitée
- ✅ Possibilité d'installer uniquement location ou vente selon les besoins
- ✅ Respect des bonnes pratiques Odoo

### Points techniques forts

**Validations et contraintes:**
- Vérification automatique de disponibilité des vélos
- Contrôle des dates (fin > début)
- Contraintes d'unicité (numéro de série)
- Validation de l'état (vélo en mauvais état non louable)

**Calculs automatiques:**
- Durée de location (heures/jours)
- Tarification selon le type
- Total avec caution
- Statistiques en temps réel

**Rapports SQL:**
- Vues matérialisées pour les rapports
- Performance optimale
- Requêtes SQL personnalisées

---

## 4️⃣ Valeur Ajoutée pour le Client

### Gains pour le magasin

**Gain de temps:**
- ✅ Plus de gestion manuelle des locations
- ✅ Calculs automatiques des tarifs
- ✅ Vérification automatique de disponibilité
- ✅ Génération automatique des contrats PDF

**Gain d'argent:**
- ✅ Optimisation du taux d'occupation (rapports)
- ✅ Pas de coûts de licence
- ✅ Réduction des erreurs de facturation
- ✅ Meilleur suivi des stocks

**Meilleure gestion:**
- ✅ Vue en temps réel de l'activité
- ✅ Historique complet client
- ✅ Rapports de performance
- ✅ Calendrier des réservations

**Évolutivité:**
- ✅ Peut gérer plusieurs magasins
- ✅ Ajout facile de nouvelles catégories de vélos
- ✅ Extensible avec d'autres modules Odoo (CRM, Marketing, etc.)

---

## 5️⃣ Questions/Réponses

### Questions probables et réponses

**Q: Combien de temps a pris le développement ?**
R: "Le développement complet a pris environ [X heures/jours], incluant la conception, le développement, les tests et la documentation. La structure modulaire d'Odoo nous a beaucoup aidés."

**Q: Est-ce que le système peut gérer plusieurs magasins ?**
R: "Oui, Odoo gère nativement le multi-entreprises/multi-magasins. Il suffirait de configurer plusieurs sociétés et entrepôts dans le système."

**Q: Que se passe-t-il si un client rend le vélo en retard ?**
R: "Le système enregistre la date de retour réelle. On peut ensuite recalculer le montant dû si nécessaire. Une évolution possible serait d'ajouter un calcul automatique de pénalités de retard."

**Q: Comment gérez-vous les dommages sur les vélos ?**
R: "Il y a un champ 'Rapport de dommages' dans le contrat de location. Le gestionnaire peut y noter les problèmes constatés. Le vélo peut ensuite être mis en maintenance."

**Q: Peut-on réserver un vélo à l'avance ?**
R: "Oui, le contrat peut être créé et confirmé avec une date de début future. Le système vérifie qu'il n'y a pas de conflit avec d'autres réservations."

**Q: Comment sauvegardez-vous les données ?**
R: "Les données sont dans PostgreSQL. On peut faire des sauvegardes régulières avec pg_dump. Avec Docker, on peut aussi sauvegarder les volumes."

**Q: Le système gère-t-il les réparations et la maintenance ?**
R: "Oui, chaque vélo a un état 'En Maintenance'. On peut y ajouter des notes internes sur les réparations effectuées. Une évolution possible serait un module dédié à la gestion de l'atelier."

**Q: Peut-on personnaliser les tarifs par client (fidélité, etc.) ?**
R: "Actuellement, les tarifs sont par catégorie de vélo. Mais Odoo permet d'ajouter des listes de prix personnalisées par client ou des programmes de fidélité via d'autres modules."

**Q: Et pour les paiements en ligne ?**
R: "Odoo supporte de nombreuses passerelles de paiement (Stripe, PayPal, etc.) via des modules additionnels. C'est une évolution facile à ajouter."

---

## 6️⃣ Conseils pour Réussir la Présentation

### Avant la présentation

- [ ] **Testez TOUT votre système** au moins 2-3 fois
- [ ] **Préparez vos données de démo** (clients, vélos, commandes)
- [ ] **Chronométrez** votre présentation (max 15 min)
- [ ] **Préparez un plan B** si internet/système ne fonctionne pas
- [ ] **Testez sur le PC de présentation** quelques heures avant
- [ ] **Fermez tous les onglets/applications inutiles**
- [ ] **Mode présentation** : agrandissez l'écran, désactivez notifications

### Pendant la présentation

**✅ À FAIRE:**
- Parler lentement et clairement
- Regarder l'audience, pas l'écran
- Utiliser des phrases courtes
- Montrer votre enthousiasme pour le projet
- Expliquer le "pourquoi" avant le "comment"
- Laisser le temps au jury de noter
- Sourire et rester professionnel

**❌ À ÉVITER:**
- Lire vos notes mot à mot
- Parler trop vite
- Utiliser trop de jargon technique
- Perdre du temps sur des détails
- Dire "euh" trop souvent
- Tourner le dos au jury
- Paniquer si quelque chose bug

### En cas de problème technique

**Si Odoo ne démarre pas:**
- Gardez votre calme
- Montrez le code source et expliquez l'architecture
- Utilisez des captures d'écran préparées à l'avance
- Expliquez ce qui devrait se passer

**Si une fonction ne marche pas:**
- Ne perdez pas de temps à débugger en live
- Passez à la suite
- Expliquez ce qui devrait se passer normalement

---

## 7️⃣ Support Visuel (Optionnel)

Si vous créez des slides PowerPoint/Google Slides:

### Slide 1: Titre
- Nom du projet
- Logo Bike Shop
- Noms des membres du groupe
- Date

### Slide 2: Contexte
- Besoins du client
- Contraintes (gratuit, local, etc.)

### Slide 3: Solution Proposée
- Schéma de l'architecture
- 2 modules personnalisés
- Technologies utilisées

### Slide 4: Fonctionnalités Principales
- Liste à puces avec icônes
- Vente, Location, Stock, Rapports

### Slide 5: Démonstration
- "Passons à la démo live..."

### Slide 6: Architecture Technique
- Diagramme des modules
- Technologies

### Slide 7: Valeur Ajoutée
- Gains pour le client
- Chiffres clés (temps gagné, etc.)

### Slide 8: Évolutions Futures
- Paiement en ligne
- Application mobile
- CRM intégré
- etc.

### Slide 9: Conclusion
- Remerciements
- Questions ?

---

## 8️⃣ Script de Présentation Complet

### Exemple de script (à adapter)

**INTRODUCTION (1 min)**

"Bonjour, je suis [Nom] et voici [Nom2]. Aujourd'hui nous allons vous présenter notre projet de système de gestion pour un magasin de vélos développé avec Odoo 19.0.

Votre besoin était de gérer à la fois la vente et la location de vélos, sans coûts de licence logiciel. Nous avons donc développé une solution complète basée sur Odoo Community Edition, qui est gratuite et open-source.

Notre système permet de gérer un catalogue de vélos et accessoires, les commandes clients, les contrats de location avec tarification automatique, et génère des rapports de performance en temps réel."

**DÉMONSTRATION (7 min)**

"Commençons par la démonstration. Voici l'interface principale de Bike Shop.

[Montrer le menu]

Notre parc comprend actuellement 6 vélos de différentes catégories : ville, VTT, route, électrique, et enfant.

[Montrer liste vélos en Kanban]

Prenons ce GIANT Road Pro. Vous voyez toutes ses caractéristiques, son état actuel, et ses statistiques de location.

[Ouvrir fiche vélo]

Maintenant créons un nouveau contrat de location.

[Créer contrat étape par étape]

Vous remarquez que :
1. Seuls les vélos disponibles sont proposés
2. La durée est calculée automatiquement
3. Le tarif s'ajuste selon le type de location choisi
4. Le total inclut automatiquement la caution

[Confirmer et démarrer]

Le vélo passe en état 'Loué' et n'est plus disponible pour une autre réservation.

Passons maintenant à la vente.

[Montrer catalogue produits]

Nous avons des vélos neufs à vendre, des accessoires comme des casques et antivols, et des pièces détachées.

[Créer commande vente]

Enfin, les rapports.

[Montrer rapports]

Ces analyses permettent d'optimiser le taux d'occupation et la stratégie tarifaire."

**TECHNIQUE (2 min)**

"Techniquement, notre solution repose sur 2 modules Python personnalisés :
- bike_shop_rental pour la location (env. 800 lignes de code)
- bike_shop_sale pour la vente (env. 400 lignes)

Nous utilisons les capacités avancées d'Odoo : calculs automatiques, vues multiples (Kanban, Calendar, Pivot), rapports SQL optimisés, et validations métier.

Le déploiement se fait via Docker, ce qui garantit un environnement reproductible et une installation en 5 minutes chrono."

**CONCLUSION (30 sec)**

"Notre solution apporte un vrai gain de productivité : plus de gestion manuelle, zéro erreur de calcul, et des rapports en temps réel. Le tout sans aucun coût de licence.

Nous sommes prêts à répondre à vos questions. Merci !"

---

## 9️⃣ Checklist Finale

### 1 semaine avant
- [ ] Code complété et testé
- [ ] README rédigé
- [ ] Code poussé sur GitHub
- [ ] Slides préparés (si utilisés)
- [ ] Script de présentation rédigé

### 1 jour avant
- [ ] Présentation répétée au moins 2 fois
- [ ] Timing vérifié
- [ ] Système testé sur PC de présentation
- [ ] Questions/réponses préparées
- [ ] Tenue professionnelle prête

### Le jour J - 30 min avant
- [ ] PC allumé et Odoo démarré
- [ ] Onglets préparés
- [ ] Mode présentation activé
- [ ] Notification désactivées
- [ ] Un verre d'eau à portée

### Juste avant de commencer
- [ ] Respirer profondément
- [ ] Sourire
- [ ] Regarder le jury
- [ ] Confiance !

---

## 🎯 Conclusion

**Vous avez créé un vrai système professionnel !**

Soyez fiers de votre travail, vous avez développé une solution complète qui répond à un vrai besoin métier. Montrez votre passion et votre maîtrise du sujet.

**Bon courage et excellente présentation ! 🚴‍♂️**
