from architecture.module import Module
from architecture.mission import Mission
import sqlite3
import config

class EmoteMission(Mission):

	emote = ""

	def initialize(self):
		emote_db = sqlite3.connect("db/emotes.db")
		cursor = emote_db.cursor()
		cursor.execute("SELECT name FROM emotes ORDER BY random() LIMIT 1")
		self.emote = cursor.fetchone()[0]
		return ("Emote mission started! The first user to type the emote " + self.emote + " wins 50 points!")

	def update(self, username, db_manager, command_args):
		if username == config.NICK:
			return
		for part in command_args:
			if part == self.emote:
				user_points = db_manager.get_user_points(username)

				if user_points == None:
					print ("The user " + username + " was not found. Creating the user in the database now")
					db_manager.create_user(username, points)
				else:
					print("Awarding user " + username + " " + str(50) + " points")
					db_manager.update_user(username, user_points + 50)
				self.result = "User " + username + " was the first to type " + self.emote + " in chat and has won 50 points!"
				self.has_finished = True

	def get_name(self):
		return "Emote Mission"