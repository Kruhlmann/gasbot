#message_queue.py

recieve_queue = []
sender_queue = []

def append_message(username, message):
	if message is not None:
		recieve_queue.append(Message(username, message))

def send(message):
	if message is not None:
		sender_queue.append(message)

class Message():
	username = ""
	message = ""

	def __init__(self, username, message):
		self.username = username;
		self.message = message;