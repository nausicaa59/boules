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
	return app.response_class(
		response=json.dumps(request.form.to_dict()),
		status=200,
		mimetype='application/json'
	)	



@app.route("/joueur/<int:id>", methods=['PUT'])
def joueurEdit(id):
	return app.response_class(
		response=json.dumps(["joueur edité " + str(id)]),
		status=200,
		mimetype='application/json'
	)



@app.route("/joueur/<int:id>", methods=['DELETE'])
def joueurDelet(id):
	return app.response_class(
		response=json.dumps(["joueur supprimé " + str(id)]),
		status=200,
		mimetype='application/json'
	)



'''
@app.route("/joueur/<int:idJoueur>")
def joueur(idJoueur):
	j = mJoueur.getFull(g.db, idJoueur)
	if j == False:
		return app.response_class(
			response=json.dumps({}),
			status=404,
			mimetype='application/json'
		)

	return app.response_class(
		response=json.dumps(j),
		status=404,
		mimetype='application/json'
	)
'''


@app.before_request
def init_app():
	g.db = model.prepareDb()
	g.mavaleur = "un test !"



@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.disconnect()
