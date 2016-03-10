#db_manager.py
import sqlite3
import json

try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

class Db_Manager():
	db = None
	emote_db = None
	cursor = None
	emote_cursor = None

	def __init__(self, channel):
		self.db = sqlite3.connect("db/" + channel + ".db")
		self.emote_db = sqlite3.connect("db/emotes.db")
		self.cursor = self.db.cursor()
		self.emote_cursor = self.emote_db.cursor()

	def create_table(self, query_string):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS " + query_string)
		self.db.commit()

	def dispose(self):
		self.db.commit()
		self.cursor.close()
		self.db.close()

	def user_exists(self, username):
		self.cursor.execute("SELECT * FROM user_points WHERE user = \'" + username + "\'")
		data = self.cursor.fetchone()
		if data is None:
			return False
		else:
			return True

	def create_user(self, username, points=0):
		try:
			if not self.user_exists(username):
				self.cursor.execute("INSERT INTO user_points VALUES ('" + username + "', " + str(points) + ")")
		except sqlite3.Error as er:
			print("Failed to create user " + username + ": " + er.message)
		self.db.commit()

	def query(self, query):
		self.cursor.execute(query)
		self.db.commit()
		return self.cursor

	def get_cursor(self):
		return self.cursor

	def get_user_points(self, user):
		username =str.lower(user)
		q = self.cursor.execute("SELECT points FROM user_points WHERE user = \'" + username + "\'")
		p = q.fetchone()
		if p == None:
			return 0
		else:
			return p[0]

	def update_user(self, username, points):
		username =str.lower(username)
		self.db.commit()
		return self.cursor.execute("UPDATE user_points SET points = " + str(points) + " WHERE user = '" + username + "'")

	#still in dev pls no userino until fixerino Kappa (validate the JSON file gotten from the twitchemotes API)
	#this version has been almost completely grabbed from pajladas github (github.com/pajlada)
	def update_emote_db(self):
		self.emote_cursor.execute("CREATE TABLE IF NOT EXISTS emotes (name TEXT, id INT)")
		self.emote_db.commit()

		url = "https://twitchemotes.com/api_cache/v2/global.json"
		response = urllib2.urlopen(url)
		data = json.loads(response.read().decode())
		emotes = data["emotes"]
		for emote in emotes:
			self.emote_cursor.execute("INSERT INTO emotes VALUES ('" + emote + "', " + str(data["emotes"][emote]["image_id"]) + ")")
			self.emote_db.commit()


	def get_user_json():
		try:
			url = "http://tmi.twitch.tv/group/user/" + config.CHAN + "/chatters"
			response = urllib2.urlopen(url)
			data = json.loads(response.read().decode())
			return data["chatters"]["viewers"]
		except:
			print("Error getting JSON from user list")
			return False

	def get_moderator_json():
		try:
			url = "http://tmi.twitch.tv/group/user/" + config.CHAN + "/chatters"
			response = urllib2.urlopen(url)
			data = json.loads(response.read().decode())
			return data["chatters"]["moderators"]
		except:
			print("Error getting JSON from user list")
			return False

	def add_points():
		self.query("UPDATE user_points SET points = points + 1")
		self.db.commit()

	def reset_points():
		self.query("UPDATE user_points SET points = 0")