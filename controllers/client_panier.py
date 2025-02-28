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
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article

    sql = "SELECT * FROM ligne_panier WHERE vetement_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    # Récupérer les infos du vêtement et son stock
    sql = "SELECT * FROM vetement WHERE id_vetement = %s"
    mycursor.execute(sql, (id_article,))
    vetement = mycursor.fetchone()

    if article_panier and article_panier['quantite'] >= 1:
        if vetement['stock'] >= int(quantite):
            # Mettre à jour la quantité dans le panier
            sql = "UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND vetement_id = %s"
            mycursor.execute(sql, (quantite, id_client, id_article))
            
            # Mettre à jour le stock
            sql = "UPDATE vetement SET stock = stock - %s WHERE id_vetement = %s"
            mycursor.execute(sql, (quantite, id_article))
        else:
            flash("Stock insuffisant pour cette quantité")
    else:
        if vetement['stock'] >= int(quantite):
            # Ajouter au panier
            sql = "INSERT INTO ligne_panier (utilisateur_id, vetement_id, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp)"
            mycursor.execute(sql, (id_client, id_article, quantite))
            
            # Mettre à jour le stock
            sql = "UPDATE vetement SET stock = stock - %s WHERE id_vetement = %s"
            mycursor.execute(sql, (quantite, id_article))

    get_db().commit()

    # Pour l'affichage du panier
    sql = """
    SELECT ligne_panier.*, vetement.nom, vetement.prix, vetement.stock 
    FROM ligne_panier 
    JOIN vetement ON ligne_panier.vetement_id = vetement.id_vetement 
    WHERE ligne_panier.utilisateur_id = %s
    """
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    prix_total = sum(article['prix'] * article['quantite'] for article in articles_panier)

    return render_template(
        'client/boutique/_panier.html',
        articles_panier=articles_panier,
        prix_total=prix_total
    )

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = ''' selection de la ligne du panier pour l'article et l'utilisateur connecté'''
    article_panier=[]

    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = ''' mise à jour de la quantité dans le panier => -1 article '''
    else:
        sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'article disponible
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'article pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

    get_db().commit()
    return redirect('/client/article/show')


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
