from architecture.module import Module
import config
import winsound

class SoundModule(Module):


	def play_sound(username, db_manager, command_args):
		if len(command_args) < 2:
			sounds = ""
			for sound in config.sounds:
				sounds += sound + ", "
			return("The list of sounds are currently: " + sounds)
		else:
			points = db_manager.get_user_points(username)

			if points >= config.SOUND_COST:
				if command_args[1] in config.sounds:
					db_manager.update_user(username, points - config.SOUND_COST)
					print("Playing sound " + "sound/" + command_args[1] + ".wav")
					winsound.PlaySound("sound/" + command_args[1] + ".wav", winsound.SND_FILENAME)
					return(None)
				else:
					return("The sound " + command_args[1] +  " is not in the library! You have not been charged any points.")
			else:
				return("Sorry " + username + " you need " + str(config.SOUND_COST) + " points to play a sound! (You have " + points + ")")

	def play_premium_sound(username, db_manager, command_args):
		if len(command_args) < 2:
			sounds = ""
			for sound in config.premium_sounds:
				sounds += sound + ", "
			return("The list of premium sounds are currently: " + sounds)
		else:
			points = db_manager.get_user_points(username)

			if points >= config.PREMIUM_SOUND_COST:
				if command_args[1] in config.premium_sounds:
					db_manager.update_user(username, points - config.PREMIUM_SOUND_COST)
					print("Playing premium sound " + "sound/" + command_args[1] + ".wav")
					winsound.PlaySound("sound/" + command_args[1] + ".wav", winsound.SND_FILENAME)
					return(None)
				else:
					return("The premium sound " + command_args[1] +  " is not in the library! You have not been charged any points.")
			else:
				return("Sorry " + username + " you need " + str(config.PREMIUM_SOUND_COST) + " points to play a premium sound! (You have " + points + ")")

	def play_sound_combo(username, db_manager, command_args):
		if len(command_args) < 2:
			sounds = ""
			for sound in config.sound_combos:
				combo_n = str.split(sound, ";")[0] + " "
				sounds += combo_n
			return("The list of sounds combos are currently: " + sounds)
		else:
			points = db_manager.get_user_points(username)

			if points >= config.PREMIUM_SOUND_COST:
				found_combo = 0
				combo_name = ""

				for combo in config.sound_combos:
					combo = str.split(combo, ";")
					combo_name = combo[0]
					if combo_name == command_args[1]:
						found_combo = 1
						break

				if found_combo == 1:
					for combo in config.sound_combos:
						combo = str.split(combo, ";")
						combo_name = combo[0]

						if combo_name == command_args[1]:
							db_manager.update_user(username, points - config.SOUND_COMBO_COST)
							print("Playing sound combo " + combo_name)
							winsound.PlaySound("sound/" + combo[1] + ".wav", winsound.SND_FILENAME)
							winsound.PlaySound("sound/" + combo[2] + ".wav", winsound.SND_FILENAME)
							return(None)
				else:
					return("The sound combo " + command_args[1] +  " is not in the library! You have not been charged any points.")
			else:
				return("Sorry " + username + " you need " + str(config.SOUND_COMBO_COST) + " points to play a premium sound! (You have " + points + ")")

	functions = {
		"!playsound" : play_sound,
		"!premiumsound" : play_premium_sound,
		"!playcombo" : play_sound_combo,
	}

	def update(self, username, db_manager, command_args):
		if command_args[0] in self.functions:
			return self.functions[command_args[0]](username, db_manager, command_args)

def isInt(s):
    try: 
        return int(s)
    except ValueError:
        return False