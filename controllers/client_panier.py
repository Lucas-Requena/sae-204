#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    quantite = request.form.get('quantite', 1, type=int)
    
    if id_article is None or quantite <= 0:
        flash(u'Erreur lors de l\'ajout au panier', 'alert-danger')
        return redirect('/client/article/show')
    
    # Vérifier le stock disponible
    sql = '''SELECT stock FROM vetement WHERE id_vetement = %s'''
    mycursor.execute(sql, (id_article,))
    result = mycursor.fetchone()
    
    if not result:
        flash(u'Article non trouvé', 'alert-danger')
        return redirect('/client/article/show')
    
    stock_disponible = result['stock']
    
    # Vérifier si l'article est déjà dans le panier
    sql = '''SELECT quantite FROM ligne_panier 
             WHERE utilisateur_id = %s AND vetement_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    panier_item = mycursor.fetchone()
    
    if panier_item:
        # L'article est déjà dans le panier, mettre à jour la quantité
        nouvelle_quantite = panier_item['quantite'] + quantite
        
        # Vérifier si le stock est suffisant
        if nouvelle_quantite > stock_disponible:
            flash(f'Stock insuffisant. Stock disponible: {stock_disponible}', 'alert-warning')
            return redirect('/client/article/show')
        
        # Mettre à jour la quantité dans le panier
        sql = '''UPDATE ligne_panier 
                 SET quantite = %s 
                 WHERE utilisateur_id = %s AND vetement_id = %s'''
        mycursor.execute(sql, (nouvelle_quantite, id_client, id_article))
    else:
        # L'article n'est pas dans le panier, l'ajouter
        # Vérifier si le stock est suffisant
        if quantite > stock_disponible:
            flash(f'Stock insuffisant. Stock disponible: {stock_disponible}', 'alert-warning')
            return redirect('/client/article/show')
        
        # Ajouter l'article au panier
        sql = '''INSERT INTO ligne_panier (utilisateur_id, vetement_id, quantite) 
                 VALUES (%s, %s, %s)'''
        mycursor.execute(sql, (id_client, id_article, quantite))
    
    # Mettre à jour le stock
    sql = '''UPDATE vetement 
             SET stock = stock - %s 
             WHERE id_vetement = %s'''
    mycursor.execute(sql, (quantite, id_article))
    
    get_db().commit()
    flash(u'Article ajouté au panier', 'alert-success')
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    
    if id_article is None:
        flash(u'Erreur lors de la suppression de l\'article', 'alert-danger')
        return redirect('/client/panier/show')
    
    # Récupérer la quantité actuelle dans le panier
    sql = '''SELECT quantite FROM ligne_panier 
             WHERE utilisateur_id = %s AND vetement_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    panier_item = mycursor.fetchone()
    
    if not panier_item:
        flash(u'Article non trouvé dans le panier', 'alert-danger')
        return redirect('/client/panier/show')
    
    quantite_actuelle = panier_item['quantite']
    
    if quantite_actuelle > 1:
        # Réduire la quantité de 1
        sql = '''UPDATE ligne_panier 
                 SET quantite = quantite - 1 
                 WHERE utilisateur_id = %s AND vetement_id = %s'''
        mycursor.execute(sql, (id_client, id_article))
        quantite_a_retourner = 1
    else:
        # Supprimer l'article du panier
        sql = '''DELETE FROM ligne_panier 
                 WHERE utilisateur_id = %s AND vetement_id = %s'''
        mycursor.execute(sql, (id_client, id_article))
        quantite_a_retourner = 1
    
    # Remettre la quantité dans le stock
    sql = '''UPDATE vetement 
             SET stock = stock + %s 
             WHERE id_vetement = %s'''
    mycursor.execute(sql, (quantite_a_retourner, id_article))
    
    get_db().commit()
    flash(u'Article retiré du panier', 'alert-success')
    return redirect('/client/panier/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    
    if id_article is None:
        flash(u'Erreur lors de la suppression de la ligne', 'alert-danger')
        return redirect('/client/panier/show')
    
    # Récupérer la quantité actuelle dans le panier
    sql = '''SELECT quantite FROM ligne_panier 
             WHERE utilisateur_id = %s AND vetement_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    panier_item = mycursor.fetchone()
    
    if not panier_item:
        flash(u'Article non trouvé dans le panier', 'alert-danger')
        return redirect('/client/panier/show')
    
    quantite_a_retourner = panier_item['quantite']
    
    # Supprimer la ligne du panier
    sql = '''DELETE FROM ligne_panier 
             WHERE utilisateur_id = %s AND vetement_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    
    # Remettre la quantité dans le stock
    sql = '''UPDATE vetement 
             SET stock = stock + %s 
             WHERE id_vetement = %s'''
    mycursor.execute(sql, (quantite_a_retourner, id_article))
    
    get_db().commit()
    flash(u'Ligne supprimée du panier', 'alert-success')
    return redirect('/client/panier/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    
    # Récupérer tous les articles du panier pour remettre les quantités en stock
    sql = '''SELECT vetement_id, quantite FROM ligne_panier 
             WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    panier_items = mycursor.fetchall()
    
    # Remettre les quantités en stock
    for item in panier_items:
        sql = '''UPDATE vetement 
                 SET stock = stock + %s 
                 WHERE id_vetement = %s'''
        mycursor.execute(sql, (item['quantite'], item['vetement_id']))
    
    # Vider le panier
    sql = '''DELETE FROM ligne_panier 
             WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    
    get_db().commit()
    flash(u'Panier vidé', 'alert-success')
    return redirect('/client/panier/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
