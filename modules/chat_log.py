from architecture.module import Module
from missions.emote import EmoteMission
from time import strftime
import config

class ChatLogModule(Module):

	def update(self, username, db_manager, command_args):
		log_user_message(username, command_args)

def log_user_message(username, command_args):
	message = username + ": "
	for part in command_args:
		message += part + " "

	log_file = open("logs/" + username + ".txt", "w")
	log_file.write(strftime("%Y-%m-%d %H:%M:%S") + " " + message)
	log_file.close()