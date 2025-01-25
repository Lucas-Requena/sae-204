#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_vetement = Blueprint('client_vetement', __name__,
                        template_folder='templates')

@client_vetement.route('/client/vetement/show')
def show_vetements():
    mycursor = get_db().cursor()
    selected_types = request.args.getlist('type_vetement[]')
    
    sql = '''
    SELECT vetement.*, type_vetement.libelle_type_vetement
    FROM vetement
    LEFT JOIN type_vetement ON vetement.type_vetement_id = type_vetement.id_type_vetement
    '''
    
    params = []
    if selected_types:
        sql += ' WHERE type_vetement.id_type_vetement IN (%s)' % ','.join(['%s'] * len(selected_types))
        params.extend(selected_types)
    
    sql += ' ORDER BY vetement.nom_vetement'
    
    mycursor.execute(sql, tuple(params) if params else None)
    vetements = mycursor.fetchall()

    sql_types = '''
    SELECT * FROM type_vetement
    ORDER BY libelle_type_vetement
    '''
    mycursor.execute(sql_types)
    types_vetement = mycursor.fetchall()

    return render_template('client/boutique/vetements.html',
                         vetements=vetements,
                         items_filtre=types_vetement)

@client_vetement.route('/client/index')
@client_vetement.route('/client/vetement/show')
def client_vetement_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''   selection des articles   '''
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    articles =[]


    # pour le filtre
    types_article = []


    articles_panier = []

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )

@client_vetement.route('/client/vetement/details/<int:id>')
def details(id):
    mycursor = get_db().cursor()
    
    sql = '''
    SELECT vetement.*
    FROM vetement
    WHERE vetement.id_vetement = %s
    '''
    mycursor.execute(sql, (id,))
    vetement = mycursor.fetchone()

    if not vetement:
        abort(404)

    return render_template('client/boutique/details_vetement.html',
                         vetement=vetement)
