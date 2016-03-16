from architecture.module import Module
import time
from includes.termcolor import colored, cprint

class SubscriberModule(Module):

	def update(self, username, db_manager, command_args):
		if username == "twitchnotify":
			if "subscribed" in command_args:
				if command_args[1] == "just":
					return("Welcome " + command_args[0] + " to the bub club! Raise your ruwBub everyone!")
				else:
					return("Welcome back to the bub club " + command_args[0] + " for " + command_args[3] + " years in a row PogChamp")
