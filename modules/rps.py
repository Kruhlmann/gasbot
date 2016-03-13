from architecture.module import Module
import random

class RPSModule(Module):

	tie = " it's a tie ResidentSleeper"
	bot_win = " I win, you suck EleGiggle"
	user_win = " you win, never am i ever lucky DansGame"

	def update(self, username, db_manager, command_args):
		if command_args[0] == "!rps":
			i = random.randint(0, 2)
			bot_pick_text = ""
			if i == 0:
				bot_pick_text = "rock"
			elif i == 1:
				bot_pick_text = "paper"
			else:
				bot_pick_text = "scissors"
			if len(command_args) < 2:
				return ("Pick rock, paper or scissors (!rps " + bot_pick_text + ")")
			else:
				user_pick = command_args[1]
				if user_pick == "rock":
					if bot_pick_text == "rock":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.tie
					if bot_pick_text == "paper":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.bot_win
					if bot_pick_text == "scissors":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.user_win
				elif user_pick == "paper":
					if bot_pick_text == "rock":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.user_win
					if bot_pick_text == "paper":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.tie
					if bot_pick_text == "scissors":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.bot_win
				elif user_pick == "scissors":
					if bot_pick_text == "rock":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.bot_win
					if bot_pick_text == "paper":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.user_win
					if bot_pick_text == "scissors":
						return "Result: [" + user_pick + " vs " + bot_pick_text + "] " + username +  self.tie
				else:
					return command_args[1] + " is not a fair pick " + username + " DansGame"
