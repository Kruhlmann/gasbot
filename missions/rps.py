from architecture.mission import Mission
import config
import event_overview

class RPSMission(Mission):

	def initialize(self):
		event_overview.latest_rps_winner = ""
		return ("RPS mission started! The first user to win a match of Rock, Paper, Scissors against the bot wins " + str(self.prize) + " points! (!rps rock/paper/scissors)")

	def update(self, username, db_manager, command_args):
		if event_overview.latest_rps_winner != "":
				user_points = db_manager.get_user_points(username)

				if user_points == None:
					print ("The user " + username + " was not found. Creating the user in the database now")
					db_manager.create_user(username)
				else:
					print("Awarding user " + username + " " + str(self.prize) + " points")
					db_manager.update_user(username, user_points + self.prize)
				self.result = "User " + event_overview.latest_rps_winner + " was the first to win a rock, paper, scissors battles versus me and has won " + str(self.prize) + " points!"
				self.has_finished = True

	def get_name(self):
		return "RPS Mission"