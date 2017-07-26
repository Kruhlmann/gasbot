from architecture.module import Module
from random import randint

class AutismModule(Module):

	def update(self, username, db_manager, command_args):
		if command_args[0] == "!autism":
			sender = username
			if len(command_args) > 1:
				sender = command_args[1]
			randLevel = randint(0,100)
			if str.lower(sender) == "tkeey":
				randLevel = randint(80,100)
			emote = ""
			if randLevel <= 30:
				emote = "FeelsGoodMan"
			elif randLevel <= 75:
				emote = "FeelsBadMan"
			else:
				emote = "EleGiggle"
			return(sender + " is " + str(randLevel) + "%" + " autistic " + emote)