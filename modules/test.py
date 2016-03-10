from architecture.module import Module

class TestModule(Module):

	def update(self, username, db_manager, command_args):
		if username == "gasolinebased":
			return "Kappa"