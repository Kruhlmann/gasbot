#message_queue.py

recieve_queue = []
send_queue = []

def append_message(username, message):
	recieve_queue.append(Message(username, message))

class Message():
	username = ""
	message = ""

	def __init__(self, username, message):
		self.username = username;
		self.message = message;