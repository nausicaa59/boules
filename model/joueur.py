import pymysql
import datetime
import json
import time
from .validation import vJoueur
from pony.orm import *


@db_session
def getFull(db, idCible):
	try:
		auteur = db.Joueur[idCible]
		auteurDic = auteur.to_dict_prepara()
		auteurDic["participations"] = [x.to_dict_prepara() for x in auteur.participations]
		return (True, auteurDic)
	except Exception as e:
		return (False, "aucun joueur trouvé")



@db_session
def getAll(db):
	try:
		joueurs = []
		queryJoueurs = select((j, count(j.participations), max(j.participations.challenge.date_start)) for j in db.Joueur) \
					  .order_by(lambda j,c,p: (j.nom, j.prenom))
		
		for x in queryJoueurs:
			joueur = x[0].to_dict_prepara()
			joueur["nbChallenge"] = x[1]
			joueur["lastParticipation"] = x[2].strftime('%Y-%m-%d %H:%M:%S') if x[2] != None else "-"
			joueurs.append(joueur)
		return (True, joueurs)
	except Exception as e:
		return (False, [str(e)])



@db_session
def create(db, data):
	try:		
		return (True, joueurs)
	except Exception as e:
		return (False, [str(e)])
