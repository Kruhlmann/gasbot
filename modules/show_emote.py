from architecture.module import Module
import hashlib
import config
import socket
import random

class ShowEmoteModule(Module):

	s = None

	def __init__(self, name):
		self.name = name
		self.s = socket.socket()
		self.s.connect((config.HOST, config.PORT))
		self.s.send(("PASS " + config.PASS + "\r\n").encode())
		self.s.send(("NICK " + config.NICK + "\r\n").encode())
		self.s.send(("JOIN #" + "420blazeitdawg" + " \r\n").encode())

	def update(self, username, db_manager, command_args):
		if command_args[0] == "!showemote":
			points = db_manager.get_user_points(username)
			if points >= config.DISPLAY_EMOTE_COST:
				db_manager.update_user(username, points - config.DISPLAY_EMOTE_COST)
				self.s.send(("PRIVMSG #420blazeitdawg :" + get_random_hash() + ":" + command_args[1] + "\r\n").encode())
			else:
				return(username + " you need " + str(config.DISPLAY_EMOTE_COST) + " points to display an emote; you have " + str(points) + " points FeelsBadMan")

def get_random_hash():
	return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()