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

try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

def recive_thread(s):
	MOTD = False
	point_timer = int(round(time.time() * 1000))
	readbuffer = ""

	# Connecting to Twitch IRC by passing credentials and joining a certain channel 
	
	
	print("RECIEV THREAD: ONLINE #" + config.CHAN)

	while True:
		readbuffer = readbuffer + s.recv(1024).decode()
		temp = str.split(readbuffer, "\n")
		readbuffer = temp.pop()
		time.sleep(0.1)
		for line in temp:
			if (line[0] == "PING"):
				s.send(("PONG %s\r\n" % line[1]).encode())
			else:
				# Splits the given string so we can work with it better 
				parts = str.split(line, ":")

				if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
					try:
						# Sets the message variable to the actual message sent 
						message = parts[2][:len(parts[2]) - 1]
					except:
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
	db_manager.create_table("`user_points`(user TEXT, points INT)")
	db_manager.update_emote_db()
	module_manager = ModuleManager()

	#ADD MODULES
	module_manager.add_module(TestModule("Test module"))
	module_manager.add_module(AutismModule("Autism meter"))
	module_manager.add_module(PointsCommandsModule("Point commands"))
	module_manager.add_module(SoundModule("Sounds"))
	module_manager.add_module(MissionsModule("Missions"))
	module_manager.add_module(UptimeModule("Uptime", time.time()))
	module_manager.add_module(PointGeneratorModule("Point generator", time.time()))
	module_manager.add_module(TimeOutModule("Timeout"))

	while True:
		while len(message_queue.recieve_queue) > 0:
			message = message_queue.recieve_queue[0].message
			username = message_queue.recieve_queue[0].username

			#PROCESS MESSAGE
			try:
				print("> " + username + ": " + message)
			except:
				print("> UTF-8 error")
				continue

			command_args = str.split(message, " ")
			module_manager.update_modules(username, db_manager, command_args)

			#Create user if not exists
			if not db_manager.user_exists(username):
				db_manager.create_user(username)
				message_queue.send_queue.append("Welcome " + username + "! You have now been registered in the database and will start earning points! PogChamp")
			
			#REMOVE MESSAGEz
			del message_queue.recieve_queue[0]

def sender_thread(s):

	def send_message(message):
		if message == None:
			return
		message_queue.recieve_queue.append(Message(config.NICK, message))
		s.send(("PRIVMSG #" + config.CHAN + " :" + message + "\r\n").encode())

	print("SENDER THREAD: ONLINE #" + config.CHAN)

	while True:
		for i in range(0, len(message_queue.sender_queue)):
			if(message_queue.sender_queue[0] is not None):
				send_message(message_queue.sender_queue[0])
			del message_queue.sender_queue[0]
			time.sleep(1.5) 


if __name__ == "__main__":
	s = socket.socket()
	s.connect((config.HOST, config.PORT))
	s.send(("PASS " + config.PASS + "\r\n").encode())
	s.send(("NICK " + config.NICK + "\r\n").encode())
	s.send(("JOIN #" + config.CHAN + " \r\n").encode())

	recive_thread = threading.Thread(target=recive_thread, args=(s,))
	module_thread = threading.Thread(target=module_thread, args=(s,))
	sender_thread = threading.Thread(target=sender_thread, args=(s,))
	recive_thread.start()
	module_thread.start()
	sender_thread.start()