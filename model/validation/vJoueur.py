from cerberus import Validator
from . import vTools



'''
============================================
Joueur
============================================
'''

schema = {
	'nom'		: {'type': 'string', 'empty': False,'required' : True},
	'prenom'	: {'type': 'string', 'empty': False, 'required' : True},
	'pseudo'	: {'type': 'string', 'empty': False, 'required' : True},
	'password'	: {'type': 'string', 'empty': False, 'required' : True},
	'email'		: {'type': 'string', 'empty': False, 'required' : True, 'validator': vTools.isEmail}
}


def validate(candidat):
	v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(candidat) == False :
		return v.errors
	return True
