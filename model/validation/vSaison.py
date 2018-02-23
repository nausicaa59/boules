from cerberus import Validator
import vTools



'''
============================================
Joueur
============================================
'''

schema = {
	'date_start': {'type': 'string', 'empty': False,'required' : True, 'validator': vTools.isDate},
	'date_close': {'type': 'string', 'empty': False,'required' : True, 'validator': vTools.isDate}
}


def validate(candidat):
	v = Validator(schema, allow_unknown = True, error_handler=vTools.TranslateError)
	if v.validate(candidat) == False :
		return v.errors
	return True



'''
print(validate({
	'date_start': '2014-01-01 05:05:05',
	'date_close': {}
}))
'''