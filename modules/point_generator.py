from architecture.module import Module
import time
import config

class PointGeneratorModule(Module):

	point_time = 0

	def __init__(self, name, point_time):
		self.name = name;
		self.point_time = point_time

	def update(self, username, db_manager, command_args):
		while time.time() - self.point_time > config.POINT_INTERVAL:
			self.point_time += config.POINT_INTERVAL
			db_manager.query("UPDATE user_points SET points = points + 1")