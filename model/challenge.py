import pymysql
import json
import time
import validus
from datetime import datetime
from pony.orm import *
from cerberus import Validator
from . import vTools


schema = {
	'nom'			: {'type': 'string', 'empty': False, 'required' : True},
	'date_start'	: {'type': 'string', 'empty': False, 'required' : True},
	'saison'		: {'type': 'integer', 'empty': False, 'required' : True}
}


def validerCandidat(db, c):
	v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(c) == False :
		return (False, v.errors)
	
	if validus.istime(c["date_start"], '%Y-%m-%d') == False:
		return (False, {"date_start" : "La date n'est pas valide"})

	return (True, {})


@db_session
def getAllBySaison(db, idSaison):
	try:
		challenges = []
		queryChallenges = select((c, count(c.participations)) for c in db.Challenge if c.saison == db.Saison[idSaison]) \
					  .order_by(lambda c,b: desc(c.date_start))

		for x in queryChallenges:
			challenge = x[0].to_dict_prepara()
			challenge["saison"] = x[0].saison.to_dict_prepara()
			challenge["nb_joueur"] = x[1]
			challenges.append(challenge)
		return (True, challenges)
	except Exception as e:
		return (False, [str(e)])


@db_session
def getFull(db, idCible):
	try:
		challenge = db.Challenge[idCible]
		challengeDic = challenge.to_dict_prepara()
		challengeDic["saison"] = challenge.saison.to_dict_prepara()
		challengeDic["participations"] = [x.to_dict_prepara() for x in challenge.participations]
		return (True, challengeDic)
	except Exception as e:
		return (False, str(e))



@db_session
def create(db, c):
	try:
		c['saison'] = db.Saison[c['saison']]
		saison = db.Challenge(**c, created_at = datetime.now(), updated_at = datetime.now())		
		return (True, saison.to_dict_prepara())
	except Exception as e:
		return (False, [str(e)])


'''
v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(candidat) == False :
		return v.errors
	return True
'''