from architecture.module import Module
from random import randint
import config

class PointsCommandsModule(Module):

	def get_user_points(username, db_manager, command_args):
		sender = username
		if len(command_args) > 1:
			sender = command_args[1]
		user_points = db_manager.get_user_points(sender)
		if user_points == None:
			return ("The user " + sender + " was not found. Creating the user in the database now")
			db_manager.create_user(sender)
		else:
			return ("User " + sender + " has " + str(user_points) + " points")	

	def roulette(username, db_manager, command_args):
		if len(command_args) < 2:
			return (username + " you need to specify an amount to roll [!roulette 37]")
		else:
			if not isInt(command_args[1]):
				return (username + " your syntax is invalid! Try something like this [!roulette 37]")
			gamble = int(command_args[1])
			user_points = db_manager.get_user_points(username)
			if user_points == None:
				return (username + " you dont exist in the database. creating you now")
				db_manager.create_user(username)
			else:
				if user_points < gamble:
					return ("Sorry " + username + " you only have " + str(user_points) + " points")
				else:
					roll = randint(5, 100)
					if roll < 50:
						db_manager.update_user(username, user_points + gamble)
						return (username + " just won " + str(gamble) + " points in the roulette FeelsGoodMan")
					else:
						db_manager.update_user(username, user_points - gamble)
						return (username + " just lost " + str(gamble) + " points in the roulette FeelsBadMan")						

	def give_points(username, db_manager, command_args):
		username = str.lower(username)
		if username == "gasolinebased":
			points = 100
			user = "gasolinebased"
			if len(command_args) > 1:
				points = isInt(command_args[1])
			if len(command_args) > 2:
				user = command_args[2]
			user_points = db_manager.get_user_points(username)

			if points == False:
				return (command_args[1] + " is not a number FailFish")
			if user_points == None:
				return ("The user " + user + " was not found. Creating the user in the database now")
				db_manager.create_user(user, points)
			else:
				db_manager.update_user(user, user_points + points)
				return ("User " + user + " was given " + str(points) + " points")
		else:
			return ("Nice try " + username + " 4Head")

	functions = {
		"!points" : get_user_points,
		"!roulette" : roulette,
		"!givepoints" : give_points,
	}

	def update(self, username, db_manager, command_args):
		if command_args[0] in self.functions:
			return self.functions[command_args[0]](username, db_manager, command_args)

def isInt(s):
    try: 
        return int(s)
    except ValueError:
        return False
