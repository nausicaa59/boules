import re
import validus
from cerberus import errors



class TranslateError(errors.BasicErrorHandler):
	messages = errors.BasicErrorHandler.messages.copy()
	messages[errors.DOCUMENT_MISSING] = "Document manquant"
	messages[errors.REQUIRED_FIELD.code] = 'Champs requis'
	messages[errors.UNKNOWN_FIELD.code] = "Champs inconnu"
	messages[errors.DEPENDENCIES_FIELD.code] = "Le champs '{0}' est requis"
	messages[errors.DEPENDENCIES_FIELD_VALUE.code] = "dépend de ces valeurs : {constraint}"
	messages[errors.EXCLUDES_FIELD.code] = "{0} n'est pas présent dans les valeurs autorisés suivant : {field}"
	messages[errors.DOCUMENT_FORMAT] = "{0} n'est pas un document, il doit être un dictionnaire"
	messages[errors.EMPTY_NOT_ALLOWED.code] = 'Le champs ne doit pas être vide'
	messages[errors.NOT_NULLABLE.code] = 'Le champs ne doit pas être null'
	messages[errors.BAD_TYPE.code] = "Le champs doit être du type : {constraint}"
	messages[errors.BAD_TYPE_FOR_SCHEMA.code] = "Le schema doit être un dictionnaire"
	messages[errors.ITEMS_LENGTH.code] = "La longueur de la liste doit être de {constraint}, elle est actuellement de {0}"
	messages[errors.MIN_LENGTH.code] = "La longueur minimal doit être : {constraint}"
	messages[errors.MAX_LENGTH.code] = "La longueur maximal doit être : {constraint}"
	messages[errors.REGEX_MISMATCH.code] = "La valeur n'a pas matcher pour l'expression suivante : {constraint}"
	messages[errors.MIN_VALUE.code] = "La valeur minimal doit être : {constraint}"
	messages[errors.MAX_VALUE.code] = "La valeur maximal doit être : {constraint}"
	messages[errors.UNALLOWED_VALUE.code] = "Valeur non autorisée : {value}"
	messages[errors.UNALLOWED_VALUES.code] = "Valeurs non autorisées : {0}"
	#messages[errors.CUSTOM.code] = ""
	#messages[errors.FORBIDDEN_VALUE.code] = ""
	#messages[errors.FORBIDDEN_VALUES.code] = ""
	#messages[errors.NORMALIZATION.code] = ""
	#messages[errors.COERCION_FAILED.code] = ""
	#messages[errors.RENAMING_FAILED.code] = ""
	#messages[errors.READONLY_FIELD.code] = ""
	#messages[errors.SETTING_DEFAULT_FAILED.code] = ""
	#messages[errors.ERROR_GROUP.code] = ""
	#messages[errors.MAPPING_SCHEMA.code] = ""
	#messages[errors.SEQUENCE_SCHEMA.code] = ""
	#messages[errors.KEYSCHEMA.code] = ""
	#messages[errors.VALUESCHEMA.code] = ""
	#messages[errors.BAD_ITEMS.code] = ""
	#messages[errors.LOGICAL.code] = ""
	#messages[errors.NONEOF.code] = ""
	#messages[errors.ONEOF.code] = ""
	#messages[errors.ANYOF.code] = ""
	#messages[errors.ALLOF.code] = ""



def clean(fonction_a_decorer):
     def cleanWrapper(*args, **kwargs):
        result = fonction_a_decorer(*args, **kwargs)
        if isinstance(result, dict) == False:
        	return result
        return result

     return cleanWrapper



def isDate(field, value, error):
    if validus.istime(value, '%Y-%m-%d %H:%M:%S') == False:
        error(field, "Le champs n'est pas une date valide")



def isEmail(field, value, error):
    if validus.isemail(value) == False:
        error(field, "Le champs n'est pas un email non valide")