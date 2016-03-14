from architecture.module import Module
from custom.commands import command_list
import config
import sqlite3

class CustomCommandsModule(Module):

	commands_db = None
	commands_cursor = None

	def __init__(self, name):
		self.name = name
		self.commands_db = sqlite3.connect("db/" + config.CHAN + "_commands")
		self.commands_cursor = self.commands_db.cursor()
		self.commands_cursor.execute("CREATE TABLE IF NOT EXISTS commands (trigger TEXT, body TEXT)")

	def update(self, username, db_manager, command_args):
		if username == config.NICK:
			return None
		if command_args[0] == "!addcomm":
			cmd_trigger = command_args[1]
			cmd_body = ""
			for i in range(2, len(command_args)):
				cmd_body += command_args[i] + " "
			self.commands_cursor.execute("INSERT INTO commands VALUES (\'" + cmd_trigger + "\', \'" + cmd_body + "\')")
			self.commands_db.commit()


		for key, value in command_list.items():
			if command_args[0] == key:
				return value.replace("$username", username)
			

	def stop_watch(self):
		seconds = time.time() - self.start_time;
		minutes = 0
		hours = 0
		while seconds > 60:
			seconds -= 60
			minutes += 1
		while minutes > 60:
			minutes -= 60
			hours += 1
		return hours, minutes, round(seconds)