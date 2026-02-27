-- =====================================================
-- Base de données : Centre Culturel Douta Seck
-- Gestion des réservations de la salle polyvalente
-- =====================================================

CREATE DATABASE douta_seck;
USE douta_seck;

-- TABLE : utilisateurs
CREATE TABLE utilisateurs (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    nom_complet VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'GESTIONNAIRE', 'VISITEUR') NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- TABLE : groupes
CREATE TABLE groupes (
    id_groupe INT AUTO_INCREMENT PRIMARY KEY,
    nom_groupe VARCHAR(100) NOT NULL,
    responsable VARCHAR(100) NOT NULL,
    type_evenement ENUM('Atelier', 'Réunion', 'Conférence', 'Cours') NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- TABLE : creneaux
CREATE TABLE creneaux (
    id_creneau INT AUTO_INCREMENT PRIMARY KEY,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    CONSTRAINT chk_heure CHECK (heure_fin > heure_debut)
);


-- TABLE : reservations
CREATE TABLE reservations (
    id_reservation INT AUTO_INCREMENT PRIMARY KEY,
    date_reservation DATE NOT NULL,
    id_creneau INT NOT NULL,
    id_groupe INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_creneau)
        REFERENCES creneaux(id_creneau)
        ON DELETE CASCADE,

    FOREIGN KEY (id_groupe)
        REFERENCES groupes(id_groupe)
        ON DELETE CASCADE,

    UNIQUE (date_reservation, id_creneau)
);


INSERT INTO creneaux (heure_debut, heure_fin) VALUES
('09:00:00', '11:00:00'),
('11:00:00', '13:00:00'),
('14:00:00', '16:00:00'),
('16:00:00', '18:00:00');

