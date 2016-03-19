from architecture.module import Module
from missions.emote import EmoteMission
from missions.rps import RPSMission
import config

class MissionsModule(Module):

	current_mission = None

	def update(self, username, db_manager, command_args):
		if self.current_mission is not None:
			self.current_mission.update(username, db_manager, command_args)
			if self.current_mission.has_finished:
				result = self.current_mission.execute_result(username, db_manager, command_args)
				self.current_mission = None
				return result
		else:
			if command_args[0] == "!startmission":
				requested_mission = command_args[1]
				print("User " + username + " wanted to start mission: " + requested_mission)
				if username == config.CHAN or username == "gasolinebased":
					if requested_mission == "emote":
						self.current_mission = EmoteMission(username, 50)
						return self.current_mission.initialize()
					if requested_mission == "rps":
						self.current_mission = RPSMission(username, 50)
						return self.current_mission.initialize()
				else:
					return("Nice try " + username + "! I bet you're a TF2 player EleGiggle Only gasolinebased or the broadcaster can start missions")
			if command_args[0] == "!cancelmission":
				if username == config.CHAN or username == "gasolinebased":
					self.current_mission = None
					return "Active mission has been canceled DatSheffy"
				else:
					return("Nice try " + username + "! I bet you're a TF2 player EleGiggle Only gasolinebased or the broadcaster can start missions")

def isInt(s):
    try: 
        return int(s)
    except ValueError:
        return False