from architecture.module import Module
from custom.commands import command_list
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
			db_manager.query("INSERT INTO commands VALUES (\'" + cmd_trigger + "\', \'" + cmd_body + "\')")
			db_manager.db.commit()
			return "Command " + cmd_trigger + " added!"


		for key, value in command_list.items():
			if command_args[0] == key:
				return value.replace("$username", username)

		q = db_manager.query("SELECT body FROM commands WHERE trigger=\'" + command_args[0] + "\'")
		p = q.fetchone()
		if p == None:
			return None
		else:
			return format_command(p[0], username)

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

def format_command(command, username):
	return command.replace("$username", username)