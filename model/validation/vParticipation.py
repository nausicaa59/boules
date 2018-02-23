from cerberus import Validator
import vTools



'''
============================================
Joueur
============================================
'''

schema = {
	'challenge_id'		: {'type': 'integer', 'empty': False, 'required' : True},
	'joueur_id'			: {'type': 'integer', 'empty': False, 'required' : True},
	'partie_gaghante'	: {'type': 'integer', 'empty': False, 'required' : True},
	'goal'				: {'type': 'integer', 'empty': False, 'required' : True}
}


def validate(candidat):
	v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(candidat) == False :
		return v.errors
	return True


'''
print(validate({
	'challenge_id'		: 5,
	'joueur_id'			: 45,
	'partie_gaghante'	: 3,
	'goal'				: 45
}))
'''


