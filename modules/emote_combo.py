from architecture.module import Module

class EmoteComboModule(Module):

	current_emote = ""
	emote_count = 0

	def update(self, username, db_manager, command_args):
		#Not implemented yet
		
		return None
		for part in command_args:
			print(part + " " + str(db_manager.is_emote(part)))
			if db_manager.is_emote(part):
				if part == self.current_emote:
					self.emote_count += 1
					if self.emote_count % 10 == 0:
							return "PogChamp the emote " + self.current_emote + " has been spammed " + str(self.emote_count) + " times in a row!"
					break
				else:
					self.current_emote = part
					self.emote_count = 0
					break

def isInt(s):
    try: 
        return int(s)
    except ValueError:
        return False