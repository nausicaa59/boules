import pymysql
import json
import time
import validus
from datetime import datetime
from pony.orm import *
from cerberus import Validator
from . import vTools


schema = {
	'nom'		: {'type': 'string', 'empty': False,'required' : True},
	'prenom'	: {'type': 'string', 'empty': False, 'required' : True},
	'pseudo'	: {'type': 'string', 'empty': False, 'required' : True},
	'password'	: {'type': 'string', 'empty': False, 'required' : True},
	'email'		: {'type': 'string', 'empty': True, 'required' : True},
	'actif'		: {'type': 'integer', 'empty': False, 'required' : True, 'allowed' : [0,1]},
}


@db_session
def getFull(db, idCible):
	try:
		auteur = db.Joueur[idCible]
		auteurDic = auteur.to_dict_prepara()
		auteurDic["participations"] = [x.to_dict_prepara() for x in auteur.participations]
		return (True, auteurDic)
	except Exception as e:
		return (False, ["aucun joueur trouvé"])



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
def isUniqueEmail(db, e):
	joueur = select(j for j in db.Joueur if j.email == e)
	if count(joueur) == 0:
		return True
	else:
		return False



@db_session
def create(db, j):
	try:
		joueur = db.Joueur(**j, created_at = datetime.now(), updated_at = datetime.now())		
		return (True, joueur.to_dict_prepara())
	except Exception as e:
		return (False, [str(e)])



@db_session
def update(db, id, d):
	try:
		d["updated_at"] = updated_at = datetime.now()
		joueur = db.Joueur[id]
		joueur.set(**d)		
		return (True, joueur.to_dict_prepara())
	except Exception as e:
		return (False, [str(e)])



@db_session
def delete(db, j):
	try:
		db.Joueur[j].delete()	
		return (True, ["Suppression du joueur réussi"])
	except Exception as e:
		return (False, [str(e)])



def validerCandidat(db, c):
	v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(c) == False :
		return (False, v.errors)

	if c["email"] != "" and validus.isemail(c["email"]) == False:
		return (False, {"email" : "L'email non valide"})

	return (True, {})






'''
v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(candidat) == False :
		return v.errors
	return True
'''