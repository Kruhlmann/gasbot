from architecture.module import Module
import sqlite3
import time
import config
from random import randint

class DuelModule(Module):

	def update(self, username, db_manager, command_args):
		if command_args[0] == "!duel":
			if len(command_args) < 3 or isInt(command_args[2]) == False:
				return(username + ", you need to use the syntax: !duel username amount FailFish")
			else:
				return(self.request_duel(username, command_args[1], command_args[2], db_manager))
		if command_args[0] == "!accept":
			return(self.accept_duel(username, db_manager))


	def request_duel(self, duelist1, duelist2, amount, db_manager):
		amount = int(amount)
		duelist1_points = db_manager.get_user_points(duelist1)
		duelist2_points = db_manager.get_user_points(duelist2)
		if duelist1_points < amount:
			return("Sorry " + duelist1 + ", you requested a duel for " + str(amount) + " points but you only have " + str(duelist1_points) + " FeelsBadMan")
		if duelist2_points < amount:
			return("Sorry " + duelist1 + ", you requested a duel for " + str(amount) + " points but your opponent only has " + str(duelist2_points) + " FeelsBadMan")
		db_manager.query("SELECT * FROM duels WHERE duelist1=\'" + duelist1 + "\' AND duelist2=\'" + duelist2 + "\'")
		if db_manager.get_cursor().fetchone() is not None:
			return (duelist1 + " you have already requested a duel with " + duelist2)
		else:		
			db_manager.query("SELECT * FROM duels WHERE duelist2=\'" + duelist2 + "\'")
			if db_manager.get_cursor().fetchone():
				return (duelist2 + " already has a duel pending!")
			else:
				db_manager.query("INSERT INTO duels VALUES (\'" + duelist1 + "\', \'" + duelist2 + "\', " + str(amount) + ")")
				return ("A duel with " + duelist2 + " has been requested for " + str(amount) + " points by " + duelist1)
	
	#'duelist2' has accepted the duel
	def accept_duel(self, duelist1, db_manager):
		print(duelist1 + " has accepted a duel!")
		points = db_manager.get_user_points(duelist1)

		db_manager.query("SELECT * FROM duels WHERE duelist2=\'" + duelist1 + "\'")
		data = db_manager.get_cursor().fetchone()
		if data is not None:
			opponent = data[0]
			amount = data[2]
			if amount > points:
				return (duelist1 + " you only have " + str(points) + " points and can't accept this duel for " +str(amount) + " points")
			else:
				if randint(0, 99) < 50:
					db_manager.update_user(duelist1, db_manager.get_user_points(duelist1) + amount)
					db_manager.update_user(opponent, db_manager.get_user_points(opponent) - amount)
					return (duelist1 + " just won " + str(amount) + " from " + opponent)
				else:
					db_manager.update_user(duelist1, db_manager.get_user_points(duelist1) - amount)
					db_manager.update_user(opponent, db_manager.get_user_points(opponent) + amount)
					return (duelist1 + " just lost " + str(amount) + " against " + opponent)
				db_manager.query("DELETE FROM duels WHERE duelist2=\'" + duelist1 + "\'")
		else:
			return (duelist1 + " you currently have no duels pending")

def isInt(s):
    try: 
        return int(s)
    except ValueError:
        return False