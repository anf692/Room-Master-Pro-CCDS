# Application de Gestion d’une Salle Polyvalente

Application console en Python pour administrer les réservations de la salle polyvalente du Centre Culturel Douta Seck, en s'appuyant sur une base de données relationnelle. avec gestion des rôles utilisateurs et export du planning journalier.

---

## Fonctionnalités

### Gestion des utilisateurs
- Inscription
- Connexion / Déconnexion
- Gestion des rôles :
  - **ADMIN**
  - **GESTIONNAIRE**
  - **VISITEUR**
- Vérification des permissions avant chaque action

### Gestion du planning
- Affichage du planning journalier
- Réservation d’un créneau
- Vérification des conflits de réservation
- Affichage des créneaux libres

### Gestion des groupes
- Ajouter un groupe
- Association d’un groupe à une réservation
- Vérification des doublons

### Export
- Export du planning journalier au format **CSV**

---


### Principe d’architecture

- Séparation claire des responsabilités
- Logique métier dans les services
- Vérification des rôles côté service (sécurité)
- Interface console dans `Application`

---

## Base de données

### Tables principales :

- `utilisateurs`
- `groupes`
- `creneaux`
- `reservations`

### Relations :

- Un utilisateur possède un rôle
- Un groupe peut réserver plusieurs créneaux
- Un créneau peut être réservé une seule fois par date

---

## Gestion des rôles

| Action | ADMIN | GESTIONNAIRE | VISITEUR |
|--------|-------|--------------|----------|
| Voir planning | ✅ | ✅ | ✅ |
| Réserver | ✅ | ✅ | ❌ |
| Ajouter groupe | ✅ | ✅ | ❌ |
| Export CSV | ✅ | ✅ | ❌ |

Les permissions sont :
- Vérifiées dans le menu
- Sécurisées dans les services (double protection)

---

## Format des dates

L’application utilise :

- Saisie utilisateur : `jj/mm/aaaa`
- Format base MySQL : `YYYY-MM-DD`

Une conversion automatique est effectuée avant toute requête SQL.

---

### Cloner le projet

```bash
git clone <url-du-projet>
cd projet