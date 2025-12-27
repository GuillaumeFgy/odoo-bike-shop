# 🎯 Guide de Démonstration - Bike Shop Odoo

## 📋 Menus Essentiels pour l'Examen

Lors de votre démonstration, concentrez-vous sur ces menus **UNIQUEMENT** :

### ✅ Menu "Bike Shop" (Menu Principal)

#### 1. **Location** ⭐ ESSENTIEL
- **Contrats de Location** : Gérer les locations de vélos
  - Créer, confirmer, démarrer, terminer une location
  - Créer des factures après retour
  - Voir l'historique complet
- **Vélos** : Consulter les vélos disponibles

#### 2. **Rapports** ⭐ ESSENTIEL
- **Analyse des Locations** : Graphiques et tableaux croisés dynamiques
  - Vue Graphique : Revenus par catégorie
  - Vue Pivot : Analyse multidimensionnelle
  - Filtres et groupements
- **Taux d'Occupation** : Performance des vélos
  - Nombre de locations par vélo
  - Revenus générés
  - Durée moyenne de location

#### 3. **Configuration** ⭐ IMPORTANT
- **Catégories de Vélos** : VTT, Route, Électrique, Ville, Enfant
- **Marques** : Giant, Trek, Specialized, etc.

---

## ❌ Menus à IGNORER (Non essentiels)

### Menus Odoo Standard (ne PAS montrer) :

- ❌ **Inventory** / **Stock** : Géré automatiquement, pas besoin de montrer
- ❌ **Invoicing** : Factures créées automatiquement depuis les locations
- ❌ **Sales** : Module séparé (bike_shop_sale), optionnel
- ❌ **Settings** : Configuration technique, pas pour la démo
- ❌ **Apps** : Installation de modules, pas pour la démo

---

## 🎬 Scénario de Démonstration Recommandé

### Étape 1 : Introduction (2 min)
1. Montrer le menu principal "Bike Shop"
2. Expliquer la structure : Location, Rapports, Configuration

### Étape 2 : Créer une Location (5 min)
1. **Bike Shop → Location → Contrats de Location → Créer**
2. Sélectionner un client (ou en créer un)
3. Choisir un vélo disponible
4. Définir les dates (début/fin)
5. Montrer le calcul automatique :
   - Durée affichée en "X jours Y heures"
   - Type de location (horaire/journalier/hebdomadaire/mensuel)
   - Tarif calculé automatiquement
   - Total avec caution
6. **Confirmer** le contrat
7. **Démarrer** la location (vélo passe en "loué")
8. Montrer que le vélo n'est plus disponible pour d'autres locations
9. **Terminer** la location (retour du vélo)
10. **Créer la facture** (seulement après le retour)

### Étape 3 : Consulter les Rapports (3 min)
1. **Bike Shop → Rapports → Analyse des Locations**
   - Montrer le graphique en barres (revenus par catégorie)
   - Basculer en vue Pivot
   - Ajouter des filtres (période, état)
2. **Bike Shop → Rapports → Taux d'Occupation**
   - Montrer les vélos les plus loués
   - Revenus par vélo
   - Durée moyenne de location

### Étape 4 : Configuration (2 min)
1. **Bike Shop → Configuration → Catégories**
   - Montrer les 5 catégories
   - Expliquer les tarifs par défaut
2. **Bike Shop → Configuration → Marques**
   - Montrer les marques prédéfinies
   - Créer une nouvelle marque (optionnel)

---

## ✨ Points Clés à Mettre en Avant

### 1. **Validations Automatiques**
- ❌ Impossible de créer une facture avant le retour du vélo
- ❌ Erreur si date de fin ≤ date de début
- ❌ Erreur si le vélo est déjà loué pour la période

### 2. **Calculs Automatiques**
- ✅ Durée calculée en jours/heures (pas en décimal)
- ✅ Tarif adapté selon le type de location
- ✅ Total avec caution

### 3. **Workflow Complet**
- Draft → Confirmed → Ongoing → Done
- Vélo disponible → loué → disponible
- États clairs et transitions logiques

### 4. **Reporting Avancé**
- Graphiques interactifs
- Tableaux croisés dynamiques (Pivot)
- Filtres et groupements
- Export Excel/PDF

---

## 🚫 Erreurs à Éviter

### Ne PAS :
1. ❌ Montrer le menu "Inventory" ou "Stock"
2. ❌ Créer une facture avant le retour du vélo
3. ❌ Modifier les configurations techniques (Settings)
4. ❌ Montrer l'onglet "Lien Produit" dans les vélos (masqué)
5. ❌ Utiliser les menus Odoo standards non pertinents

### À la place :
1. ✅ Rester dans le menu "Bike Shop"
2. ✅ Suivre le workflow complet : Confirmer → Démarrer → Terminer → Facturer
3. ✅ Montrer les rapports et analyses
4. ✅ Expliquer les validations et calculs automatiques

---

## 📝 Checklist Avant la Démo

- [ ] Module `bike_shop_rental` installé
- [ ] Données de démonstration chargées
- [ ] Au moins 3 vélos disponibles
- [ ] Au moins 2 clients créés
- [ ] Au moins 1 location "Done" pour les rapports
- [ ] Mode développeur DÉSACTIVÉ
- [ ] Navigateur en mode plein écran
- [ ] Menus non essentiels ignorés

---

## 🎯 Objectifs de l'Examen

**Important** : L'examen évalue votre capacité à :
1. **Comprendre** le problème métier
2. **Concevoir** une solution Odoo adaptée
3. **Implémenter** les fonctionnalités clés
4. **Présenter** de manière claire et professionnelle

**Ce qui compte** :
- ✅ Logique métier correcte
- ✅ Validations appropriées
- ✅ Interface utilisateur claire
- ✅ Workflow complet fonctionnel

**Ce qui compte MOINS** :
- ❌ Design graphique sophistiqué
- ❌ Fonctionnalités avancées non demandées
- ❌ Complexité technique excessive

---

## 💡 Conseils

1. **Pratiquez le scénario** 2-3 fois avant l'examen
2. **Chronométrez-vous** : 10-15 minutes max pour la démo
3. **Préparez vos réponses** aux questions potentielles
4. **Restez simple** : ne montrez que ce qui est demandé
5. **Soyez confiant** : vous avez un système fonctionnel !

---

Bonne chance pour votre examen ! 🚀
