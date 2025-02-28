#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS ligne_commande;'''
    mycursor.execute(sql)
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS ligne_panier;'''
    mycursor.execute(sql)
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS vetement;'''
    mycursor.execute(sql)
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS type_vetement;'''
    mycursor.execute(sql)
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS taille;'''
    mycursor.execute(sql)
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS commande ;'''
    mycursor.execute(sql)
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS etat ;'''
    mycursor.execute(sql)
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS utilisateur ;'''
    mycursor.execute(sql)
    sql='''
    CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
                            login VARCHAR(255),
                            email VARCHAR(255),
                            nom VARCHAR(255),
                            password VARCHAR(255),
                            role VARCHAR(255),
                            PRIMARY KEY (id_utilisateur)
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql=''' INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
                                                                          (1,'admin','admin@admin.fr',
                                                                           'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
                                                                           'ROLE_admin','admin'),
                                                                          (2,'client','client@client.fr',
                                                                           'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
                                                                           'ROLE_client','client'),
                                                                          (3,'client2','client2@client2.fr',
                                                                           'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
                                                                           'ROLE_client','client2');'''
    mycursor.execute(sql)

    sql='''CREATE TABLE taille(
                              id_taille INT AUTO_INCREMENT,
                              libelle_taille VARCHAR(255),
                              PRIMARY KEY (id_taille)
)DEFAULT CHARSET utf8;'''
    mycursor.execute(sql)
    sql=''' 
INSERT INTO taille (id_taille, libelle_taille) VALUES
                                                  (1, 'S'),
                                                  (2, 'M'),
                                                  (3, 'L'),
                                                  (4, 'XL'),
                                                  (5, 'XXL'),
                                                  (6, 'XXXL');'''
    mycursor.execute(sql)

    sql='''CREATE TABLE type_vetement(
                              id_type_vetement INT AUTO_INCREMENT,
                              libelle_type_vetement VARCHAR(255),
                              PRIMARY KEY (id_type_vetement)
)DEFAULT CHARSET utf8;'''
    mycursor.execute(sql)
    sql=''' 
INSERT INTO type_vetement (id_type_vetement, libelle_type_vetement) VALUES
                                                                        (1, 'Teeshirt'),
                                                                        (2, 'Pantalon'),
                                                                        (3, 'Pull'),
                                                                        (4, 'Veste');'''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE etat(
                     id_etat INT AUTO_INCREMENT,
                     libelle VARCHAR(255),
                     PRIMARY KEY (id_etat)
)DEFAULT CHARSET utf8;'''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO etat (id_etat, libelle) VALUES
                                        (1, 'attente'),
                                        (2, 'expédié'),
                                        (3, 'validé'),
                                        (4, 'confirmé');'''
    mycursor.execute(sql)

    sql = ''' 
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
)DEFAULT CHARSET utf8;'''
    mycursor.execute(sql)
    sql = ''' 
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
'''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commande(
                         id_commande INT AUTO_INCREMENT,
                         date_achat DATE,
                         utilisateur_id INT,
                         etat_id INT,
                         PRIMARY KEY (id_commande),
                         foreign key (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                         foreign key (etat_id) REFERENCES etat(id_etat)
)DEFAULT CHARSET utf8;
'''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
                                                                            (1, '2024-12-19',3,4),
                                                                            (2, '2025-01-21',3,3),
                                                                            (3, '2024-11-12',2,3),
                                                                            (4, '2024-7-29',2,2),
                                                                            (5, '2025-01-11',2,1),
                                                                            (6, '2025-01-01',2,1),
                                                                            (7, '2024-08-15',3,2),
                                                                            (8, '2025-02-10',3,2),
                                                                            (9, '2024-09-05',2,3),
                                                                            (10, '2024-10-30',3,3),
                                                                            (11, '2024-12-01',2,3),
                                                                            (12, '2025-03-18',3,4),
                                                                            (13, '2024-11-25',2,4),
                                                                            (14, '2025-01-31',3,4),
                                                                            (15, '2024-10-10',2,4),
                                                                            (16, '2024-07-05',2,2),
                                                                            (17, '2024-08-22',3,2),
                                                                            (18, '2025-02-25',3,1),
                                                                            (19, '2024-09-18',3,1),
                                                                            (20, '2025-03-05',2,1);

'''
    mycursor.execute(sql)

    sql = ''' CREATE TABLE ligne_commande(
                               commande_id INT,
                               vetement_id INT,
                               prix FLOAT,
                               quantite INT,
                               PRIMARY KEY (commande_id,vetement_id),
                               FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
                               FOREIGN KEY (vetement_id) REFERENCES vetement(id_vetement)
)DEFAULT CHARSET utf8;'''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ligne_commande (commande_id, vetement_id, prix, quantite) VALUES
                                                                          (1, 2, 70, 25),
                                                                          (1, 9, 50, 14),
                                                                          (1, 13, 140, 10),
                                                                          (1, 1, 50, 10),
                                                                          (1, 5, 120, 25),
                                                                          (1, 10, 200, 8),
                                                                          (2, 2, 90, 15),
                                                                          (2, 6, 60, 20),
                                                                          (2, 12, 150, 12),
                                                                          (2, 4, 80, 18),
                                                                          (2, 8, 200, 22),
                                                                          (2, 14, 130, 9),
                                                                          (3, 6, 90, 16),
                                                                          (3, 11, 40, 7),
                                                                          (3, 15, 150, 14),
                                                                          (3, 3, 40, 18),
                                                                          (3, 8, 80, 7),
                                                                          (3, 14, 110, 13),
                                                                          (4, 4, 35, 30),
                                                                          (4, 9, 140, 16),
                                                                          (4, 15, 170, 21),
                                                                          (4, 7, 50, 13),
                                                                          (4, 10, 120, 28),
                                                                          (4, 12, 175, 17),
                                                                          (5, 3, 40, 20),
                                                                          (5, 8, 60, 12),
                                                                          (5, 14, 190, 9),
                                                                          (5, 1, 60, 5),
                                                                          (5, 7, 95, 10),
                                                                          (5, 11, 130, 12),
                                                                          (6, 2, 45, 40),
                                                                          (6, 5, 70, 18),
                                                                          (6, 13, 120, 25),
                                                                          (6, 1, 85, 24),
                                                                          (6, 9, 75, 16),
                                                                          (7, 13, 180, 11),
                                                                          (7, 2, 35, 19),
                                                                          (7, 6, 125, 13),
                                                                          (7, 12, 200, 6),
                                                                          (7, 3, 55, 14),
                                                                          (7, 10, 200, 20),
                                                                          (7, 14, 85, 19),
                                                                          (8, 5, 33, 24),
                                                                          (8, 8, 75, 9),
                                                                          (8, 12, 140, 17),
                                                                          (8, 4, 65, 15),
                                                                          (8, 10, 40, 29),
                                                                          (8, 15, 120, 8),
                                                                          (9, 1, 40, 29),
                                                                          (9, 9, 160, 23),
                                                                          (9, 15, 190, 13),
                                                                          (9, 5, 170, 11),
                                                                          (9, 7, 60, 14),
                                                                          (9, 11, 100, 30),
                                                                          (10, 3, 40, 21),
                                                                          (10, 8, 75, 9),
                                                                          (10, 13, 190, 17),
                                                                          (10, 6, 50, 11),
                                                                          (10, 11, 125, 30),
                                                                          (10, 12, 175, 15),
                                                                          (11, 1, 80, 27),
                                                                          (11, 4, 70, 18),
                                                                          (11, 10, 130, 22),
                                                                          (11, 6, 50, 16),
                                                                          (11, 12, 150, 8),
                                                                          (11, 14, 85, 18),
                                                                          (12, 2, 40, 27),
                                                                          (12, 9, 180, 7),
                                                                          (12, 15, 200, 15),
                                                                          (12, 3, 30, 26),
                                                                          (12, 7, 150, 31),
                                                                          (12, 14, 190, 8),
                                                                          (13, 3, 40, 20),
                                                                          (13, 5, 140, 6),
                                                                          (13, 15, 200, 11),
                                                                          (14, 6, 100, 19),
                                                                          (14, 8, 35, 7),
                                                                          (14, 12, 170, 12),
                                                                          (15, 7, 60, 21),
                                                                          (15, 9, 90, 14),
                                                                          (15, 13, 180, 13),
                                                                          (16, 1, 65, 28),
                                                                          (16, 3, 45, 18),
                                                                          (16, 10, 200, 22),
                                                                          (17, 2, 120, 30),
                                                                          (17, 5, 50, 26),
                                                                          (17, 14, 160, 9),
                                                                          (18, 4, 75, 12),
                                                                          (18, 7, 130, 15),
                                                                          (18, 12, 180, 17),
                                                                          (19, 6, 35, 31),
                                                                          (19, 9, 85, 5),
                                                                          (19, 15, 150, 8),
                                                                          (20, 8, 60, 19),
                                                                          (20, 11, 105, 20),
                                                                          (20, 13, 200, 6);'''
    mycursor.execute(sql)


    sql = ''' 
   CREATE TABLE ligne_panier(
                             utilisateur_id INT,
                             vetement_id INT,
                             quantite INT,
                             date_ajout DATE,
                             PRIMARY KEY (utilisateur_id,vetement_id),
                             FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                             FOREIGN KEY (vetement_id) REFERENCES vetement(id_vetement)
)DEFAULT CHARSET utf8;  
         '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
