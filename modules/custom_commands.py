from architecture.module import Module
from custom.commands import command_list
from random import randint
import config
import sqlite3

class CustomCommandsModule(Module):

	def update(self, username, db_manager, command_args):
		if username == config.NICK:
			return None
		if command_args[0] == "!addcommand":
			cmd_trigger = command_args[1]
			cmd_body = ""
			for i in range(2, len(command_args)):
				cmd_body += command_args[i] + " "
			db_manager.query("INSERT INTO commands VALUES (\'" + cmd_body + "\', \'" + cmd_trigger + "\')")
			db_manager.db.commit()
			return "Command " + cmd_trigger + " added!"


		for key, value in command_list.items():
			if command_args[0] == key:
				return format_command(key, value, username)

		q = db_manager.query("SELECT body FROM commands WHERE trigger=\'" + command_args[0] + "\'")
		if q == None:
			return None
		else:
			p = q.fetchone()
			if p is not None:
				return format_command(command_args[0], p[0], username)
			return None

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

def format_command(command_name, command, username):
	print("User " + username + " requested an execution of the custom command '" + command_name)
	command = command.replace("$username", username)
	command = command.replace("$percentage", str(randint(0,100)) + "%" ) 
	return command