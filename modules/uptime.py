from architecture.module import Module
import time

class UptimeModule(Module):

	start_time = 0

	def __init__(self, name, start_time):
		self.name = name;
		self.start_time = start_time

	def update(self, username, db_manager, command_args):
		if command_args[0] == "!uptime":
			hours, minutes, seconds = self.stop_watch()
			return ("I have been online for " + str(hours) + " hours " + str(minutes) + " minutes and " + str(seconds) + " seconds MrDestructoid")

	def stop_watch(self):
		seconds = time.time() - self.start_time;
		print(str(time.time()) + " " + str(self.start_time))
		minutes = 0
		hours = 0
		while seconds > 60:
			seconds -= 60
			minutes += 1
		while minutes > 60:
			minutes -= 60
			hours += 1
		return hours, minutes, round(seconds)