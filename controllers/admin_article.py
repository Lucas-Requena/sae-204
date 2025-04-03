#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash, session
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''SELECT vetement.id_vetement AS id_article, 
                    vetement.nom_vetement AS nom, 
                    vetement.prix_vetement AS prix, 
                    vetement.description, 
                    vetement.photo AS image, 
                    vetement.stock,
                    type_vetement.libelle_type_vetement AS type, 
                    taille.libelle_taille AS taille
             FROM vetement
             JOIN type_vetement ON vetement.type_vetement_id = type_vetement.id_type_vetement
             JOIN taille ON vetement.taille_id = taille.id_taille
             ORDER BY vetement.nom_vetement'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    
    # Récupération des types de vêtements
    sql = '''SELECT id_type_vetement, libelle_type_vetement 
             FROM type_vetement 
             ORDER BY libelle_type_vetement'''
    mycursor.execute(sql)
    types_vetement = mycursor.fetchall()
    
    # Récupération des tailles
    sql = '''SELECT id_taille, libelle_taille 
             FROM taille 
             ORDER BY id_taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    return render_template('admin/article/add_article.html',
                           types_vetement=types_vetement,
                           tailles=tailles)


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_vetement_id = request.form.get('type_vetement_id', '')
    taille_id = request.form.get('taille_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    matiere = request.form.get('matiere', '')
    fournisseur = request.form.get('fournisseur', '')
    marque = request.form.get('marque', '')
    stock = request.form.get('stock', 0)
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''INSERT INTO vetement(nom_vetement, prix_vetement, taille_id, type_vetement_id, 
                                 matiere, description, fournisseur, marque, photo, stock) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    tuple_add = (nom, prix, taille_id, type_vetement_id, matiere, description, fournisseur, marque, filename, stock)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    message = u'Article ajouté, nom: ' + nom + ' - prix: ' + prix + ' - stock: ' + str(stock)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()
    
    # Vérifier si l'article est dans une commande
    sql = '''SELECT COUNT(*) AS nb_commandes
             FROM ligne_commande
             WHERE vetement_id = %s'''
    mycursor.execute(sql, (id_article,))
    nb_commandes = mycursor.fetchone()
    
    # Vérifier si l'article est dans un panier
    sql = '''SELECT COUNT(*) AS nb_paniers
             FROM ligne_panier
             WHERE vetement_id = %s'''
    mycursor.execute(sql, (id_article,))
    nb_paniers = mycursor.fetchone()
    
    if nb_commandes['nb_commandes'] > 0 or nb_paniers['nb_paniers'] > 0:
        message = u'Cet article est présent dans des commandes ou des paniers : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        # Récupérer l'image de l'article
        sql = '''SELECT photo FROM vetement WHERE id_vetement = %s'''
        mycursor.execute(sql, (id_article,))
        article = mycursor.fetchone()
        image = article['photo']

        # Supprimer l'article
        sql = '''DELETE FROM vetement WHERE id_vetement = %s'''
        mycursor.execute(sql, (id_article,))
        get_db().commit()
        
        # Supprimer l'image si elle existe
        if image != None and os.path.exists('static/images/' + image):
            os.remove('static/images/' + image)

        message = u'Article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()
    
    # Récupérer les informations de l'article
    sql = '''SELECT id_vetement AS id_article, 
                    nom_vetement AS nom, 
                    prix_vetement AS prix, 
                    taille_id, 
                    type_vetement_id,
                    matiere, 
                    description, 
                    fournisseur, 
                    marque, 
                    photo AS image, 
                    stock
             FROM vetement
             WHERE id_vetement = %s'''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()
    
    # Récupérer les types de vêtements
    sql = '''SELECT id_type_vetement, libelle_type_vetement 
             FROM type_vetement 
             ORDER BY libelle_type_vetement'''
    mycursor.execute(sql)
    types_vetement = mycursor.fetchall()
    
    # Récupérer les tailles
    sql = '''SELECT id_taille, libelle_taille 
             FROM taille 
             ORDER BY id_taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    return render_template('admin/article/edit_article.html',
                           article=article,
                           types_vetement=types_vetement,
                           tailles=tailles)


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    id_article = request.form.get('id_article')
    nom = request.form.get('nom')
    type_vetement_id = request.form.get('type_vetement_id', '')
    taille_id = request.form.get('taille_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    matiere = request.form.get('matiere', '')
    fournisseur = request.form.get('fournisseur', '')
    marque = request.form.get('marque', '')
    stock = request.form.get('stock', 0)
    image = request.files.get('image', '')
    
    # Récupérer l'image actuelle
    sql = '''SELECT photo FROM vetement WHERE id_vetement = %s'''
    mycursor.execute(sql, (id_article,))
    image_nom = mycursor.fetchone()['photo']
    
    # Traiter la nouvelle image si fournie
    if image and image.filename:
        if image_nom and os.path.exists(os.path.join('static/images/', image_nom)):
            os.remove(os.path.join('static/images/', image_nom))
        
        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
        image_nom = filename

    # Mettre à jour l'article
    sql = '''UPDATE vetement 
             SET nom_vetement = %s, prix_vetement = %s, taille_id = %s, type_vetement_id = %s,
                 matiere = %s, description = %s, fournisseur = %s, marque = %s, photo = %s, stock = %s
             WHERE id_vetement = %s'''
    mycursor.execute(sql, (nom, prix, taille_id, type_vetement_id, matiere, description, 
                          fournisseur, marque, image_nom, stock, id_article))
    get_db().commit()

    message = u'Article modifié, nom: ' + nom + ' - prix: ' + prix + ' - stock: ' + str(stock)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/stock', methods=['GET'])
def show_stock():
    mycursor = get_db().cursor()
    sql = '''SELECT vetement.id_vetement AS id_article, 
                    vetement.nom_vetement AS nom, 
                    vetement.prix_vetement AS prix, 
                    vetement.stock,
                    type_vetement.libelle_type_vetement AS type, 
                    taille.libelle_taille AS taille,
                    (SELECT COUNT(*) FROM ligne_panier WHERE ligne_panier.vetement_id = vetement.id_vetement) AS nb_paniers
             FROM vetement
             JOIN type_vetement ON vetement.type_vetement_id = type_vetement.id_type_vetement
             JOIN taille ON vetement.taille_id = taille.id_taille
             ORDER BY vetement.stock ASC'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_stock.html', articles=articles)


@admin_article.route('/admin/article/stock/edit', methods=['GET'])
def edit_stock():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()
    
    # Récupérer les informations de l'article
    sql = '''SELECT id_vetement AS id_article, 
                    nom_vetement AS nom, 
                    prix_vetement AS prix, 
                    stock,
                    type_vetement.libelle_type_vetement AS type, 
                    taille.libelle_taille AS taille
             FROM vetement
             JOIN type_vetement ON vetement.type_vetement_id = type_vetement.id_type_vetement
             JOIN taille ON vetement.taille_id = taille.id_taille
             WHERE id_vetement = %s'''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()
    
    return render_template('admin/article/edit_stock.html', article=article)


@admin_article.route('/admin/article/stock/edit', methods=['POST'])
def valid_edit_stock():
    mycursor = get_db().cursor()
    id_article = request.form.get('id_article')
    stock = request.form.get('stock', 0)
    
    # Mettre à jour le stock de l'article
    sql = '''UPDATE vetement SET stock = %s WHERE id_vetement = %s'''
    mycursor.execute(sql, (stock, id_article))
    get_db().commit()

    message = u'Stock mis à jour pour l\'article ID: ' + id_article + ' - Nouveau stock: ' + str(stock)
    flash(message, 'alert-success')
    return redirect('/admin/article/stock')


# Ajout d'un lien direct pour modifier le stock depuis la liste des articles
@admin_article.route('/admin/article/stock/quick_edit', methods=['POST'])
def quick_edit_stock():
    mycursor = get_db().cursor()
    id_article = request.form.get('id_article')
    stock = request.form.get('stock', 0)
    
    # Mettre à jour le stock de l'article
    sql = '''UPDATE vetement SET stock = %s WHERE id_vetement = %s'''
    mycursor.execute(sql, (stock, id_article))
    get_db().commit()

    message = u'Stock mis à jour pour l\'article ID: ' + id_article + ' - Nouveau stock: ' + str(stock)
    flash(message, 'alert-success')
    
    # Rediriger vers la page d'où vient la requête
    referer = request.form.get('referer', '/admin/article/show')
    return redirect(referer)


@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
