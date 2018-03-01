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
	'date_close'	: {'type': 'string', 'empty': False, 'required' : True}
}



@db_session
def getFull(db, idCible):
	try:
		saison = db.Saison[idCible]
		saisonDic = saison.to_dict_prepara()
		saisonDic["challenges"] = [x.to_dict_prepara() for x in saison.challenges]
		return (True, saisonDic)
	except Exception as e:
		return (False, "saison introuvable")



@db_session
def getAll(db):
	try:
		saisons = []
		querySaisons = select((s, count(s.challenges)) for s in db.Saison) \
					  .order_by(lambda s,c: desc(s.date_start))

		for x in querySaisons:
			saison = x[0].to_dict_prepara()
			saison["nbChallenge"] = x[1]
			saisons.append(saison)
		return (True, saisons)
	except Exception as e:
		return (False, [str(e)])



@db_session
def create(db, s):
	try:
		saison = db.Saison(**s, created_at = datetime.now(), updated_at = datetime.now())		
		return (True, saison.to_dict_prepara())
	except Exception as e:
		return (False, [str(e)])



@db_session
def update(db, id, d):
	try:
		d["updated_at"] = datetime.now()
		saison = db.Saison[id]
		saison.set(**d)		
		return (True, saison.to_dict_prepara())
	except Exception as e:
		return (False, [str(e)])


@db_session
def delete(db, j):
	try:
		db.Saison[j].delete()	
		return (True, ["Suppression de la saison réussi"])
	except Exception as e:
		return (False, [str(e)])



def validerCandidat(db, c):
	v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(c) == False :
		return (False, v.errors)

	errors = {}
	if validus.istime(c["date_start"], '%Y-%m-%d') == False:
		errors["date_start"] = "La date n'est pas valide"

	if validus.istime(c["date_close"], '%Y-%m-%d') == False:
		errors["date_close"] = "La date n'est pas valide"

	if errors != {}:
		return (False, errors)

	date_start = datetime.strptime(c["date_start"], '%Y-%m-%d')
	date_close = datetime.strptime(c["date_close"], '%Y-%m-%d')
	if date_start == date_close:
		return (False, {"date_start" : "La date de début est égale à celle de fin"})
	if date_start > date_close:
		return (False, {"date_start" : "La date de début doit être supérieur à celle de fin"})

	return (True, {})


'''
v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(candidat) == False :
		return v.errors
	return True
'''