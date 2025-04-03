#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''SELECT commande.id_commande, commande.date_achat, etat.libelle, etat.id_etat AS etat_id,
                    commande.utilisateur_id, utilisateur.login, 
                    SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total,
                    SUM(ligne_commande.quantite) AS nbr_articles
             FROM commande
             JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
             JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
             JOIN etat ON commande.etat_id = etat.id_etat
             GROUP BY commande.id_commande, commande.date_achat, etat.libelle, etat.id_etat, 
                      commande.utilisateur_id, utilisateur.login
             ORDER BY commande.date_achat DESC'''

    commandes=[]
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    
    if id_commande != None:
        print(id_commande)
        sql = '''SELECT ligne_commande.commande_id AS id, vetement.id_vetement, 
                      vetement.nom_vetement AS nom, vetement.photo AS image,
                      ligne_commande.quantite, ligne_commande.prix, 
                      (ligne_commande.prix * ligne_commande.quantite) AS prix_ligne,
                      commande.etat_id
                 FROM ligne_commande
                 JOIN vetement ON ligne_commande.vetement_id = vetement.id_vetement
                 JOIN commande ON ligne_commande.commande_id = commande.id_commande
                 WHERE ligne_commande.commande_id = %s'''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()
        
        # Utilisation d'une requête SQL pour créer un objet commande_adresses avec des champs vides
        sql = '''SELECT 
                    '' AS nom_livraison, 
                    '' AS rue_livraison, 
                    '' AS code_postal_livraison, 
                    '' AS ville_livraison,
                    '' AS nom_facturation, 
                    '' AS rue_facturation, 
                    '' AS code_postal_facturation, 
                    '' AS ville_facturation
                 FROM commande
                 WHERE commande.id_commande = %s
                 LIMIT 1'''
        mycursor.execute(sql, (id_commande,))
        commande_adresses = mycursor.fetchone()
        
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        # Récupérer l'id_etat correspondant à "expédié"
        sql = '''SELECT id_etat FROM etat WHERE libelle = 'expédié' '''
        mycursor.execute(sql)
        etat_expedie = mycursor.fetchone()
        
        if etat_expedie:
            sql = '''UPDATE commande SET etat_id = %s WHERE id_commande = %s'''
            mycursor.execute(sql, (etat_expedie['id_etat'], commande_id))
            get_db().commit()
            flash(u'Commande expédiée avec succès', 'alert-success')
    return redirect('/admin/commande/show')
