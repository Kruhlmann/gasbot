class Mission():

	initiator = ""
	has_finished = False
	result = ""
	prize = 0

	def __init__(self, initiator, prize):
		self.initiator = initiator
		self.prize = prize
	
	def initialize(self):
		pass

	def update(self, username, db_manager, command_args):
		pass

	def get_name(self):
		pass

	def execute_result(self, username, db_manager, command_args):
		return self.result