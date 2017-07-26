#bot.py
from architecture.module_manager import ModuleManager
from modules.test import TestModule
from modules.autism import AutismModule
from modules.points_commands import PointsCommandsModule
from modules.sound import SoundModule
from modules.missions import MissionsModule
from modules.uptime import UptimeModule
from modules.point_generator import PointGeneratorModule
from modules.timeout import TimeOutModule
from modules.duel import DuelModule
from modules.custom_commands import CustomCommandsModule
from modules.show_emote import ShowEmoteModule
from modules.rps import RPSModule
from modules.emote_combo import EmoteComboModule
from modules.chat_log import ChatLogModule
from modules.subscriber import SubscriberModule
from modules.song_request import SongRequestModule
import event_overview

import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import _thread
import time
import random
import sys
import re
import string
import json
import sqlite3

import message_queue
from message_queue import Message
import config
from db_manager import Db_Manager
from subprocess import call
import subprocess

try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

def recive_thread(s):
	MOTD = False
	point_timer = int(round(time.time() * 1000))
	readbuffer = ""

	print("RECIEV THREAD: ONLINE #" + config.CHAN)

	while True:
		readbuffer = readbuffer + s.recv(1024).decode("utf-8")
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		time.sleep(0.1)
		for line in temp:
			line = line.strip()
			if readbuffer.find('PING') != -1:
				print("Pong!")
				s.send(("PONG :tmi.twitch.tv\r\n").encode())
			else:
				# Splits the given string so we can work with it better 
				parts = str.split(line, ":")

				if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
					try:
						# Sets the message variable to the actual message sent 
						message = ""
						for x in range(2, len(parts)):
							message += parts[x] + ":"
						message = message[:-1]
					except Exception as e:
						print("An error has occured while computiong the user message " + str(e))
						message = ""
					# Sets the username variable to the actual username 
					usernamesplit = str.split(parts[1], "!")
					username = usernamesplit[0]
					# Only works after twitch is done announcing stuff (MOTD = Message of the day) 
					if MOTD:
						if message != "":
							message_queue.append_message(username, message)
					else:
						for l in parts:
								if "End of /NAMES list" in l:
									MOTD = True

def module_thread(s):

	print("MODULE THREAD: ONLINE #" + config.CHAN)
	db_manager = Db_Manager(config.CHAN)
	#Create databases
	db_manager.create_table("`user_points`(user TEXT, points INT)")
	db_manager.create_table("`duels`(duelist1 TEXT, duelist2 TEXT, amount INT)")
	db_manager.create_table("`commands`(body TEXT, trigger TEXT)")
	db_manager.update_emote_db()

	module_manager = ModuleManager()
	#ADD MODULES
	#module_manager.add_module(TestModule("Test"))
	module_manager.add_module(AutismModule("Autism meter"))
	module_manager.add_module(PointsCommandsModule("Point commands"))
	module_manager.add_module(SoundModule("Sounds"))
	module_manager.add_module(MissionsModule("Missions"))
	module_manager.add_module(UptimeModule("Uptime", time.time()))
	module_manager.add_module(PointGeneratorModule("Point generator", time.time()))
	module_manager.add_module(TimeOutModule("Timeout"))
	module_manager.add_module(DuelModule("Duel"))
	module_manager.add_module(ShowEmoteModule("Show Emote"))
	module_manager.add_module(RPSModule("Rock, Paper, Scissors"))
	module_manager.add_module(EmoteComboModule("Emote Combo"))
	module_manager.add_module(ChatLogModule("Chat Log"))
	module_manager.add_module(SubscriberModule("Subscriber"))
	module_manager.add_module(SongRequestModule("Song Request"))

	#THIS MUST BE LAST SO CUSTOM COMMANDS DO NOT OVERRIDE THE MODULE COMMANDS
	module_manager.add_module(CustomCommandsModule("Custom Commands"))



	while True:
		while len(message_queue.recieve_queue) > 0:
			message = message_queue.recieve_queue[0].message
			username = message_queue.recieve_queue[0].username.lower()

			#PROCESS MESSAGE
			try:
				print("> " + username + ": " + message)
			except:
				print("> UTF-8 error")
				del message_queue.recieve_queue[0]
				continue

			command_args = str.split(message, " ")
			module_manager.update_modules(username, db_manager, command_args)

			#Create user if not exists
			if not db_manager.user_exists(username):
				db_manager.create_user(username)
				message_queue.send("Welcome " + username + "! You have now been registered in the database and will start earning points! PogChamp")
			
			#REMOVE MESSAGEz
			del message_queue.recieve_queue[0]

def sender_thread(s):

	def send_message(message):
		if message == None:
			return
		message_queue.recieve_queue.append(Message(config.NICK, message))
		s.send(("PRIVMSG #" + config.CHAN + " :" + message + "\r\n").encode("utf-8"))

	print("SENDER THREAD: ONLINE #" + config.CHAN)
	send_message("MrDestructoid GREETINGS HUMANS MrDestructoid")

	while True:
		for i in range(0, len(message_queue.sender_queue)):
			if(message_queue.sender_queue[0] is not None):
				send_message(message_queue.sender_queue[0])
			del message_queue.sender_queue[0]
			time.sleep(1.5) 

def pinger_thread(s):

	print("PINGER THREAD: ONLINE #" + config.CHAN)

	while True:
		s.send(("PING irc.twitch.tv").encode())
		print("Ping!")
		time.sleep(300)


def player_thread(s):
	print("PLAYER THREAD: ONLINE #" + config.CHAN)
	next_song_in = 0

	#
	# < Previous track
	# > Next track
	#
	while True:
		if event_overview.current_song == {} and len(event_overview.song_list) > 0:
			event_overview.current_song = event_overview.song_list[len(event_overview.song_list) - 1]
			next_song_in = int(round(time.time() * 1000)) + event_overview.current_song["length"] * 1000
			del event_overview.song_list[len(event_overview.song_list) - 1]
			f = open("current_song.txt", "w")
			f.write(event_overview.current_song["title"])
			f.close()
			call(["bin/mplayer.exe", event_overview.current_song["filename"], "-volume", str(config.VOLUME)], stdout=None, stderr=subprocess.STDOUT)
		if int(round(time.time() * 1000)) > next_song_in:
			event_overview.current_song = {}


if __name__ == "__main__":
	s = socket.socket()
	print("Connecting to server " + config.HOST + ":" + str(config.PORT))

	if config.PASS == "oauth:":
		print("You did not specify any password for the bot in the password.py file. Exiting...")
		exit()
	try:
		s.connect((config.HOST, config.PORT))
		#s.send(("CAP REQ :twitch.tv/membership \r\n").encode("utf-8"))
		s.send(("PASS " + config.PASS + "\r\n").encode("utf-8"))
		s.send(("NICK " + config.NICK + "\r\n").encode("utf-8"))
		s.send(("JOIN #" + config.CHAN + " \r\n").encode("utf-8"))
	except Exception:
		print("Could not connect to Twitch IRC server! Exiting...")
		exit()

	recive_thread = threading.Thread(target=recive_thread, args=(s,))
	module_thread = threading.Thread(target=module_thread, args=(s,))
	sender_thread = threading.Thread(target=sender_thread, args=(s,))
	player_thread = threading.Thread(target=player_thread, args=(s,))
	pinger_thread = threading.Thread(target=pinger_thread, args=(s,))
	print("Connecting to channel #" + config.CHAN + " with username ")
	recive_thread.start()
	module_thread.start()
	sender_thread.start()
	player_thread.start() 
	pinger_thread.start()