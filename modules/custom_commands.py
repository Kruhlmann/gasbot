from architecture.module import Module
from custom.commands import command_list
import config

class CustomCommandsModule(Module):

	def update(self, username, db_manager, command_args):
		if username == config.NICK:
			return None
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