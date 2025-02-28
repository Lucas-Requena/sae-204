DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS vetement;
DROP TABLE IF EXISTS type_vetement;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    PRIMARY KEY (id_utilisateur)
)DEFAULT CHARSET utf8;

CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(255),
    PRIMARY KEY (id_etat)
)DEFAULT CHARSET utf8;

CREATE TABLE taille(
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(255),
    PRIMARY KEY (id_taille)
)DEFAULT CHARSET utf8;

CREATE TABLE type_vetement(
    id_type_vetement INT AUTO_INCREMENT,
    libelle_type_vetement VARCHAR(255),
    PRIMARY KEY (id_type_vetement)
)DEFAULT CHARSET utf8;

CREATE TABLE vetement(
    id_vetement INT AUTO_INCREMENT,
    nom_vetement VARCHAR(255),
    prix_vetement FLOAT,
    taille_id INT,
    type_vetement_id INT,
    matiere VARCHAR(255),
    description VARCHAR(255),
    fournisseur VARCHAR(255),
    marque VARCHAR(255),
    photo VARCHAR(255),
    stock INT,
    PRIMARY KEY (id_vetement),
    FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
    FOREIGN KEY (type_vetement_id) REFERENCES type_vetement(id_type_vetement)
)DEFAULT CHARSET utf8;

CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
)DEFAULT CHARSET utf8;

CREATE TABLE ligne_commande(
    commande_id INT,
    vetement_id INT,
    prix FLOAT,
    quantite INT,
    PRIMARY KEY (commande_id, vetement_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (vetement_id) REFERENCES vetement(id_vetement)
)DEFAULT CHARSET utf8;

CREATE TABLE ligne_panier(
    utilisateur_id INT,
    vetement_id INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY (utilisateur_id, vetement_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (vetement_id) REFERENCES vetement(id_vetement)
)DEFAULT CHARSET utf8;

INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom) VALUES
(1, 'admin', 'admin@admin.fr', 'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988', 'ROLE_admin', 'admin'),
(2, 'client', 'client@client.fr', 'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349', 'ROLE_client', 'client'),
(3, 'client2', 'client2@client2.fr', 'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080', 'ROLE_client', 'client2');

INSERT INTO etat (id_etat, libelle) VALUES
(1, 'attente'),
(2, 'expédié'),
(3, 'validé'),
(4, 'confirmé');

INSERT INTO taille (id_taille, libelle_taille) VALUES
(1, 'XS'),
(2, 'S'),
(3, 'M'),
(4, 'L'),
(5, 'XL'),
(6, 'XXL'),
(7, '3XL');

INSERT INTO type_vetement (id_type_vetement, libelle_type_vetement) VALUES
(1, 'Teeshirt'),
(2, 'Pantalon'),
(3, 'Pull'),
(4, 'Veste');

INSERT INTO vetement (id_vetement, nom_vetement, prix_vetement, taille_id, type_vetement_id, matiere, description, fournisseur, marque, photo, stock) VALUES
(1, 'Blouson bomber', 50, 3, 4, 'similicuir', 'osef', 'Henitex', 'Bershka', 'Bomber.jpg', 100),
(2, 'Jean droit', 70, 1, 2, 'denim', 'Jean droit classique, confortable', 'Tissup', 'Levis', 'jean_court.jpg', 75),
(3, 'Blouson duvet', 80, 4, 4, 'plumes', 'Blouson 100% duvet', 'Cotontex', 'Zara', 'Blouson_duvet.jpg', 50),
(4, 'Pantalon chino', 50, 4, 2, 'tissu', 'Pantalon chino élégant et léger', 'Modechic', 'Zara', 'Pantalon_chino.jpg', 120),
(5, 'Sweat à capuche', 70, 3, 3, 'polyester', 'Confortable et pratique', 'Cuirtex', 'Jack&jones', 'J&J1.png', 85),
(6, 'Blouson retro', 90, 5, 4, 'velour', 'Style vintage intemporel', 'Semtex', 'Bershka', 'Blouson_retro.jpg', 60),
(7, 'Sweat à capuche', 45, 2, 3, 'coton', 'Doux et cosy', 'Sweatstyle', 'Jack&Jones', 'J&J2.png', 90),
(8, 'Pantalon de costume', 50, 4, 2, 'denim', 'Élégance décontractée', 'Classicstyle', 'Zara', 'Costume.jpg', 70),
(9, 'Pull tricoté', 65, 6, 3, 'laine', 'Chaud et stylé', 'Lainetex', 'Primark', 'image9.jpg', 40),
(10, 'Blouson coton', 100, 3, 4, 'coton', 'Protection et confort', 'TNF', 'The North Face', 'TNF.jpg', 55),
(11, 'Pantalon tech', 85, 3, 2, 'denim', 'Moderne et fonctionnel', 'Techstyle', 'Tokyo Techwear', 'tokyo_techwear.jpg', 65),
(12, 'Jean slim', 55, 1, 2, 'tissu', 'Coupe ajustée, look casual', 'Jeanstex', 'Levis', 'jean_slim.jpg', 80),
(13, 'Sweat à capuche', 70, 2, 3, 'polyester', 'Confort quotidien', 'Sweatstyle', 'Napapijri', 'napapijri.jpg', 45),
(14, 'Polo coton', 110, 3, 1, 'coton', 'Polo en coton, confortable et élégant', 'Polochic', 'Ralph Lauren', 'ralph_lauren.jpg', 30),
(15, 'T-shirt classe', 60, 4, 1, 'coton', 'Simple et élégant', 'Makeittex', 'The Kooples', 'thekooples.jpg', 95);

INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
(1, '2024-12-19', 3, 4),
(2, '2025-01-21', 3, 3),
(3, '2024-11-12', 2, 3),
(4, '2024-07-29', 2, 2),
(5, '2025-01-11', 2, 1),
(6, '2025-01-01', 2, 1),
(7, '2024-08-15', 3, 2),
(8, '2025-02-10', 3, 2),
(9, '2024-09-05', 2, 3),
(10, '2024-10-30', 3, 3);

INSERT INTO ligne_commande (commande_id, vetement_id, prix, quantite) VALUES
(1, 1, 50, 10),
(1, 5, 70, 25),
(2, 2, 70, 15),
(2, 6, 90, 20),
(3, 3, 80, 18),
(3, 8, 50, 7),
(4, 4, 50, 30),
(4, 9, 65, 16),
(5, 7, 45, 10),
(5, 11, 85, 12),
(6, 2, 70, 40),
(6, 5, 70, 18),
(7, 13, 70, 11),
(7, 2, 70, 19),
(8, 5, 70, 24),
(8, 8, 50, 9),
(9, 1, 50, 29),
(9, 9, 65, 23),
(10, 3, 80, 21),
(10, 8, 50, 9);

INSERT INTO ligne_panier (utilisateur_id, vetement_id, quantite, date_ajout) VALUES
(2, 1, 10, '2024-01-15'),
(2, 5, 20, '2024-02-10'),
(2, 7, 5, '2024-03-05'),
(2, 9, 12, '2024-04-18'),
(2, 11, 25, '2024-05-20'),
(3, 2, 8, '2024-07-05'),
(3, 4, 15, '2024-08-12'),
(3, 6, 20, '2024-09-01'),
(3, 8, 18, '2024-10-10'),
(3, 10, 10, '2024-11-25');

SELECT utilisateur.id_utilisateur,utilisateur.nom,utilisateur.email,SUM(ligne_commande.prix * ligne_commande.quantite) AS total_commande
FROM utilisateur
         INNER JOIN commande ON utilisateur.id_utilisateur = commande.utilisateur_id
         INNER JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
GROUP BY utilisateur.id_utilisateur, utilisateur.nom, utilisateur.email
ORDER BY total_commande DESC;

SELECT vetement.nom_vetement,SUM(ligne_commande.quantite) AS total_vendus
FROM vetement
         INNER JOIN ligne_commande ON vetement.id_vetement = ligne_commande.vetement_id
GROUP BY vetement.nom_vetement
ORDER BY total_vendus DESC;

SELECT type_vetement.libelle_type_vetement,SUM(ligne_commande.prix * ligne_commande.quantite) AS total_ventes
FROM type_vetement
         JOIN vetement ON type_vetement.id_type_vetement = vetement.type_vetement_id
         INNER JOIN ligne_commande ON vetement.id_vetement = ligne_commande.vetement_id
GROUP BY type_vetement.libelle_type_vetement
ORDER BY total_ventes DESC;

SELECT etat.libelle AS statut_commande,COUNT(commande.id_commande) AS nombre_commandes
FROM etat
         LEFT JOIN commande ON etat.id_etat = commande.etat_id
GROUP BY etat.libelle
ORDER BY nombre_commandes DESC;

