import pymysql
import time

import random
from . import model
from . import joueur
from datetime import datetime
from faker import Faker
from pony.orm import *

#------------------------
#Option
#------------------------
nbJoueur = 20
nbSaison = 3


#------------------------
#remove And recreate all table
#------------------------
fake = Faker('fr_FR')
db = model.prepareDb()
db.drop_all_tables(with_all_data=True)
db.create_tables()


#------------------------
#make joueurs and saison
#------------------------
joueurs = []
saisons = []

for i in range(0,nbSaison):
	saisons.append({
		"created_at"	: datetime.now(),
		"updated_at"	: datetime.now(),
		"date_start"	: datetime(2018 - i, 3, 31, 0, 0, 0),
		"date_close"	: datetime(2019 - i, 3, 30, 0, 0, 0),
		"nom"			: "Saison " + str(i+1)
	})


for _ in range(0,nbJoueur):
	joueurs.append({
		"created_at"	: datetime.now(),
		"updated_at"	: datetime.now(),
		"nom"			: fake.last_name(),
		"prenom"		: fake.first_name(),
		"pseudo"		: fake.user_name(),
		"password"		: fake.word(),
		"actif"			: 1,
		"email"			: fake.safe_email()
	})


with db_session:
	objSaisons 		= [db.Saison(**x) for x in saisons]
	objJoueurs 		= [db.Joueur(**x) for x in joueurs]


#------------------------
#make challenge
#------------------------
challenges = []

for i in range(len(objSaisons)):
	for m in range(0,5):
		challenges.append({
			"created_at"	: datetime.now(),
			"updated_at"	: datetime.now(),
			"date_start"	: datetime(2018 - i, 3 + m, 3 + m, 0, 0, 0),
			"saison"		: objSaisons[i].id,
			"nom"			: "Challenge " + str(m+1)
		})

with db_session:
	objChallenges 	= [db.Challenge(**x) for x in challenges]



#------------------------
#make participation
#------------------------
def getRandomResultatChallenge():
	nbPartieGagnante = random.randint(0,3)
	nbPartiePerdu = 3 - nbPartieGagnante
	goal = nbPartieGagnante * 13
	goal += sum([random.randint(0,12) for _ in range(0, nbPartiePerdu)])
	return (nbPartieGagnante, goal);	


participations = []
for j in objJoueurs:
	for c in objChallenges:
		randResult = getRandomResultatChallenge()
		participations.append({
			"created_at"		: datetime.now(),
			"updated_at"		: datetime.now(),
			"partie_gagnante"	: randResult[0],
			"goal"				: randResult[1],
			"challenge"			: c.id,
			"joueur"			: j.id
		})

with db_session:
	objParticipations 	= [db.Participation(**x) for x in participations]


db.disconnect()