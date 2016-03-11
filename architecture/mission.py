class Mission():

	initiator = ""
	has_finished = False
	result = ""

	def __init__(self, initiator):
		self.initiator = initiator;
	
	def initialize(self):
		pass

	def update(self, username, db_manager, command_args):
		pass

	def get_name(self):
		pass

	def execute_result(self, username, db_manager, command_args):
		return self.result