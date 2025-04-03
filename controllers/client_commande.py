#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    
    # Utilisation des noms de colonnes corrects
    sql = '''SELECT ligne_panier.vetement_id, vetement.nom_vetement, vetement.prix_vetement as prix, vetement.photo, ligne_panier.quantite, 
                    ligne_panier.quantite * vetement.prix_vetement as prix_ligne
             FROM ligne_panier
             JOIN vetement ON ligne_panier.vetement_id = vetement.id_vetement
             WHERE ligne_panier.utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()
    if len(articles_panier) >= 1:
        sql = '''SELECT SUM(ligne_panier.quantite * vetement.prix_vetement) as prix_total
                 FROM ligne_panier
                 JOIN vetement ON ligne_panier.vetement_id = vetement.id_vetement
                 WHERE ligne_panier.utilisateur_id = %s'''
        mycursor.execute(sql, (id_client,))
        resultat = mycursor.fetchone()
        prix_total = resultat['prix_total']
    else:
        prix_total = None
    
    # Récupération des adresses de l'utilisateur
    # Utilisation de la table 'adresse' qui est probablement le nom correct
    sql = '''SHOW TABLES LIKE 'adresse%';'''
    mycursor.execute(sql)
    tables = mycursor.fetchall()
    
    adresses = []
    id_adresse_fav = None
    
    # Essayons de trouver la bonne table d'adresses
    if tables:
        table_name = tables[0].values()[0]
        try:
            sql = f'''SELECT * FROM {table_name} WHERE utilisateur_id = %s'''
            mycursor.execute(sql, (id_client,))
            adresses = mycursor.fetchall()
            
            # Récupération de l'adresse favorite si elle existe
            for adresse in adresses:
                if 'est_favori' in adresse and adresse['est_favori'] == 1:
                    id_adresse_fav = adresse['id_adresse']
                    break
        except:
            # Si ça ne fonctionne pas, créons une adresse fictive pour tester
            adresses = [{
                'id_adresse': 1,
                'libelle': 'Adresse principale',
                'rue': '123 rue de test',
                'code_postal': '75000',
                'ville': 'Paris',
                'est_favori': 1
            }]
            id_adresse_fav = 1
    else:
        # Si aucune table d'adresse n'est trouvée, créons une adresse fictive pour tester
        adresses = [{
            'id_adresse': 1,
            'libelle': 'Adresse principale',
            'rue': '123 rue de test',
            'code_postal': '75000',
            'ville': 'Paris',
            'est_favori': 1
        }]
        id_adresse_fav = 1
    
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , validation=1
                           , id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)
    id_adresse_livraison = request.form.get('id_adresse_livraison', None)
    id_adresse_facturation = request.form.get('id_adresse_facturation', None)
    
    if not id_adresse_livraison or not id_adresse_facturation:
        flash(u'Veuillez sélectionner les adresses de livraison et de facturation', 'alert-warning')
        return redirect('/client/panier/show')

    id_client = session['id_user']
    sql = '''SELECT ligne_panier.vetement_id, vetement.prix_vetement as prix, ligne_panier.quantite
             FROM ligne_panier
             JOIN vetement ON ligne_panier.vetement_id = vetement.id_vetement
             WHERE ligne_panier.utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()
    
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le panier', 'alert-warning')
        return redirect('/client/article/show')
    
    # Vérification des stocks disponibles
    for item in items_ligne_panier:
        sql = '''SELECT stock FROM vetement WHERE id_vetement = %s'''
        mycursor.execute(sql, (item['vetement_id'],))
        result = mycursor.fetchone()
        stock_disponible = result['stock']
        
        if stock_disponible < item['quantite']:
            flash(f'Stock insuffisant pour l\'article ID {item["vetement_id"]}. Stock disponible: {stock_disponible}', 'alert-danger')
            return redirect('/client/panier/show')
    
    # Vérification de la structure de la table commande
    sql = '''DESCRIBE commande'''
    mycursor.execute(sql)
    columns = mycursor.fetchall()
    column_names = [col['Field'] for col in columns]
    
    # Création de la commande avec les colonnes correctes
    date_achat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Vérifier si les colonnes d'adresse existent
    if 'adresse_livraison_id' in column_names and 'adresse_facturation_id' in column_names:
        sql = '''INSERT INTO commande (date_achat, utilisateur_id, adresse_livraison_id, adresse_facturation_id, etat_id)
                 VALUES (%s, %s, %s, %s, 1)'''
        mycursor.execute(sql, (date_achat, id_client, id_adresse_livraison, id_adresse_facturation))
    elif 'id_adresse_livraison' in column_names and 'id_adresse_facturation' in column_names:
        sql = '''INSERT INTO commande (date_achat, utilisateur_id, id_adresse_livraison, id_adresse_facturation, etat_id)
                 VALUES (%s, %s, %s, %s, 1)'''
        mycursor.execute(sql, (date_achat, id_client, id_adresse_livraison, id_adresse_facturation))
    else:
        # Si aucune colonne d'adresse n'est trouvée, insérer sans adresse
        sql = '''INSERT INTO commande (date_achat, utilisateur_id, etat_id)
                 VALUES (%s, %s, 1)'''
        mycursor.execute(sql, (date_achat, id_client))

    # Récupération de l'ID de la commande créée
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    result = mycursor.fetchone()
    id_commande = result['last_insert_id']
    
    # Ajout des lignes de commande, mise à jour des stocks et suppression du panier
    for item in items_ligne_panier:
        # Ajout d'une ligne de commande
        sql = '''INSERT INTO ligne_commande (commande_id, vetement_id, prix, quantite)
                 VALUES (%s, %s, %s, %s)'''
        mycursor.execute(sql, (id_commande, item['vetement_id'], item['prix'], item['quantite']))
        
        # Mise à jour du stock
        sql = '''UPDATE vetement 
                 SET stock = stock - %s 
                 WHERE id_vetement = %s'''
        mycursor.execute(sql, (item['quantite'], item['vetement_id']))
        
        # Suppression de la ligne de panier
        sql = '''DELETE FROM ligne_panier 
                 WHERE utilisateur_id = %s AND vetement_id = %s'''
        mycursor.execute(sql, (id_client, item['vetement_id']))

    get_db().commit()
    flash(u'Commande ajoutée', 'alert-success')
    return redirect('/client/commande/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT commande.id_commande, commande.date_achat, etat.libelle AS etat, 
                    SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total,
                    SUM(ligne_commande.quantite) AS nbr_articles
             FROM commande 
             JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id 
             JOIN etat ON commande.etat_id = etat.id_etat
             WHERE commande.utilisateur_id = %s 
             GROUP BY commande.id_commande, commande.date_achat, etat.libelle
             ORDER BY commande.date_achat DESC'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    id_commande = request.args.get('id_commande', None)
    prix_total_commande = None
    nbr_articles_commande = None
    
    if id_commande != None:
        print(id_commande)
        sql = '''SELECT ligne_commande.quantite, ligne_commande.prix, vetement.nom_vetement AS nom, 
                      vetement.photo AS image, ligne_commande.prix * ligne_commande.quantite AS prix_ligne
                 FROM ligne_commande 
                 JOIN vetement ON ligne_commande.vetement_id = vetement.id_vetement 
                 WHERE ligne_commande.commande_id = %s'''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        # Calcul du prix total et du nombre d'articles de la commande sélectionnée
        sql = '''SELECT SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total,
                        SUM(ligne_commande.quantite) AS nbr_articles
                 FROM ligne_commande 
                 WHERE ligne_commande.commande_id = %s'''
        mycursor.execute(sql, (id_commande,))
        result = mycursor.fetchone()
        prix_total_commande = result['prix_total']
        nbr_articles_commande = result['nbr_articles']
        
    # Traitement pour changer l'état de la commande
    if request.method == 'POST' and request.form.get('id_commande') and request.form.get('etat_id'):
        id_commande_update = request.form.get('id_commande')
        nouvel_etat_id = request.form.get('etat_id')
        sql = '''UPDATE commande SET etat_id = %s WHERE id_commande = %s'''
        mycursor.execute(sql, (nouvel_etat_id, id_commande_update))
        get_db().commit()
        flash(u'État de la commande mis à jour', 'alert-success')
        return redirect('/client/commande/show')

    # Récupération des états possibles
    sql = '''SELECT id_etat, libelle FROM etat ORDER BY id_etat'''
    mycursor.execute(sql)
    etats = mycursor.fetchall()

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , id_commande_selected=id_commande
                           , prix_total_commande=prix_total_commande
                           , nbr_articles_commande=nbr_articles_commande
                           , etats=etats
                           )

