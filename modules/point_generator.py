from architecture.module import Module
import time
import config

class PointGeneratorModule(Module):

	point_time = 0
	users = []

	def __init__(self, name, point_time):
		self.name = name;
		self.point_time = point_time

	def update(self, username, db_manager, command_args):
		str_users = []
		for user in self.users:
			str_users.append(user.name)
			if username == user.name:
				user.last_message_time = time.time()

		if username not in str_users:
			self.users.append(User(username, time.time()))

		while time.time() - self.point_time > config.POINT_INTERVAL:
			self.point_time += config.POINT_INTERVAL
			for user in self.users:
				print("User " + user.name + " wrote their last message " + str(time.time() - user.last_message_time) + " seconds ago")
				if time.time() - user.last_message_time <= 15 * 60: #15 minutes of inactivity allowed
					db_manager.query("UPDATE user_points SET points = points + 1 WHERE user = \'" + user.name + "\'")
					print("Added points to user " + user.name)
				else:
					print("User " + user.name + " has been inactive for " + str(time.time() - user.last_message_time) + " seconds and will not recieve points")
			print("Finished adding points to acive users")

class User():

	name = ""
	last_message_time = 0

	def __init__(self, name, last_message_time):
		self.name = name
		self.last_message_time = last_message_time