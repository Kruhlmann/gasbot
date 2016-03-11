from architecture.module import Module
import message_queue
import config

class TimeOutModule(Module):

	def update(self, username, db_manager, command_args):
		if command_args[0] == "!buytimeout":
			target = ""
			if len(command_args) > 1:
				target = str.lower(command_args[1])
			else:
				return (username + " you need to specify a user to timeout [!buytimeout user]")
			points = db_manager.get_user_points(username)
			if target in config.PROTECTED_USERS:
				return (target + " is protected and can't be timed out!")
			if points >= config.TIME_OUT_COST:
				db_manager.update_user(username, points - config.TIME_OUT_COST)
				message_queue.send(username + " has timed out " + target + " for " + str(config.TIME_OUT_DURATION) + " EleGiggle")
				return ({"/timeout " + target + str(config.TIME_OUT_DURATION)})
			else:
				return("You don't have enough points to time someone out!")
			return(sender + " is " + str(randLevel) + "%" + " autistic " + emote)