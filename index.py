from flask import *
from pony.orm import *
from model import model
import model.joueur as mJoueur
app = Flask(__name__)




@app.route("/joueur", methods=['GET'])
def joueurShowList():
	joueurs = mJoueur.getAll(g.db)
	codeReponse = 200 if joueurs[0] else 500
	return app.response_class(
		response=json.dumps(joueurs[1]),
		status=codeReponse,
		mimetype='application/json'
	)



@app.route("/joueur/<int:id>", methods=['GET'])
def joueurShow(id):
	joueur = mJoueur.getFull(g.db, id)
	codeReponse = 200 if joueur[0] else 404
	return app.response_class(
		response=json.dumps(joueur[1]),
		status=codeReponse,
		mimetype='application/json'
	)



@app.route("/joueur", methods=['POST'])
def joueurCreate():
	data = request.get_json()
	validation = mJoueur.validerCandidat(g.db, data)
	if validation[0] == False:
		return app.response_class(
			response=json.dumps(validation[1]),
			status=400,
			mimetype='application/json'
		)

	creation = mJoueur.create(g.db, data)
	codeReponse = 200 if creation[0] else 500
	return app.response_class(
		response=json.dumps(creation[1]),
		status=codeReponse,
		mimetype='application/json'
	)	



@app.route("/joueur/<int:id>", methods=['PUT'])
def joueurEdit(id):
	joueur = mJoueur.getFull(g.db, id)
	if joueur[0] == False:		
		return app.response_class(
			response=json.dumps(joueur[1]),
			status=404,
			mimetype='application/json'
		)

	data = request.get_json()
	validation = mJoueur.validerCandidat(g.db, data)
	if validation[0] == False:
		return app.response_class(
			response=json.dumps(validation[1]),
			status=400,
			mimetype='application/json'
		)

	edition = mJoueur.update(g.db, id, data)
	codeReponse = 200 if edition[0] else 500
	return app.response_class(
		response=json.dumps(edition[1]),
		status=codeReponse,
		mimetype='application/json'
	)



@app.route("/joueur/<int:id>", methods=['DELETE'])
def joueurDelet(id):
	joueur = mJoueur.getFull(g.db, id)
	if joueur[0] == False:		
		return app.response_class(
			response=json.dumps(joueur[1]),
			status=404,
			mimetype='application/json'
		)

	if len(joueur[1]["participations"]) > 0:
		return app.response_class(
			response=json.dumps(["impossible de supprimer le joueur, il a déja participé a un concours"]),
			status=404,
			mimetype='application/json'
		)


	suppression = mJoueur.delete(g.db, id)
	codeReponse = 200 if suppression[0] else 500
	return app.response_class(
		response=json.dumps(suppression[1]),
		status=codeReponse,
		mimetype='application/json'
	)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.before_request
def init_app():
	g.db = model.prepareDb()
	g.mavaleur = "un test !"



@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.disconnect()



'''
def requires_auth(authorized, unauthorized):
	def logTestDecorateur(fonction_a_decorer):
		def logWrapper(*args, **kwargs):
			print(authorized, unauthorized)
			result = fonction_a_decorer(*args, **kwargs)			
			return result
		return logWrapper
	print("apres")
	return logTestDecorateur
'''