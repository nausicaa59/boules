import pymysql
import datetime
import time
from pony.orm import *


def prepareDb():
	db = Database()

	class Saison(db.Entity):
		_table_ 			= "saisons"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		date_start			= Required(datetime.datetime, 6)
		date_close			= Required(datetime.datetime, 6)
		challenges 			= Set('Challenge', reverse="saison")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 			= base["created_at"].strftime('%Y-%m-%d %H:%M:%S')
			base["updated_at"] 			= base["updated_at"].strftime('%Y-%m-%d %H:%M:%S')
			base["date_start"] 			= base["created_at"].strftime('%Y-%m-%d %H:%M:%S')
			base["date_close"] 			= base["updated_at"].strftime('%Y-%m-%d %H:%M:%S')
			return base


	class Challenge(db.Entity):
		_table_ 			= "challenges"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		date_start			= Required(datetime.datetime, 6)
		saison 				= Required(Saison, reverse="challenges")
		participations		= Set('Participation', reverse="challenge")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 			= base["created_at"].strftime('%Y-%m-%d %H:%M:%S')
			base["updated_at"] 			= base["updated_at"].strftime('%Y-%m-%d %H:%M:%S')
			base["date_start"] 			= base["created_at"].strftime('%Y-%m-%d %H:%M:%S')
			return base


	class Joueur(db.Entity):
		_table_ 			= "joueurs"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		nom					= Required(str)
		prenom				= Required(str)
		pseudo 				= Required(str)
		password			= Required(str)
		actif				= Required(int, default=1)
		email				= Required(str)
		participations		= Set('Participation', reverse="joueur")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 			= base["created_at"].strftime('%Y-%m-%d %H:%M:%S')
			base["updated_at"] 			= base["updated_at"].strftime('%Y-%m-%d %H:%M:%S')
			return base


	class Participation(db.Entity):
		_table_ 			= "participations"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		partie_gagnante		= Required(int)
		goal				= Required(int)
		challenge			= Required(Challenge, reverse="participations")
		joueur 				= Required(Joueur, reverse="participations")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 		= base["created_at"].strftime('%Y-%m-%d %H:%M:%S')
			base["updated_at"] 		= base["updated_at"].strftime('%Y-%m-%d %H:%M:%S')
			return base


	db.bind(provider='mysql', host='localhost', user='root', passwd='root', db='boules')
	db.generate_mapping(create_tables=True)
	return db

