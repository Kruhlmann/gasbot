import message_queue

class ModuleManager():
	modules = []

	def add_module(self, module):
		self.modules.append(module)

	def update_modules(self, username, db_manager, command_args):
		for module in self.modules:
			message_queue.send(module.update(username, db_manager, command_args))