from cerberus import Validator
import vTools



'''
============================================
Joueur
============================================
'''

schema = {
	'date_start': {'type': 'string'	, 'empty': False, 'required' : True},
	'saison_id'	: {'type': 'integer', 'empty': False, 'required' : True}
}


def validate(candidat):
	v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(candidat) == False :
		return v.errors
	return True


'''
print(validate({
	'date_start': '2014-01-01 05:05:05',
	'saison_id': 15
}))
'''

