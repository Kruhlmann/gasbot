from architecture.module import Module
import config
import urllib.parse as urlparse
import urllib
import pafy
import os.path
import re
import event_overview
class SongRequestModule(Module):

	# https://www.youtube.com/watch?v=EWF8Nfm-LLk&list=PL7XlqX4npddfrdpMCxBnNZXg2GFll7t5y&index=7
	def update(self, username, db_manager, command_args):
		if command_args[0] == "!sr" or command_args[0] == "!songrequest":
			if len(command_args) < 2:
				return "Usage: !songrequest https://www.youtube.com/watch?v=KMFLnlg883I"
			else:
				# TODO: More params should make a youtube query
				video_id = ""
				video = None
				input = command_args[1]
				if(input.startswith("http")):
					try:
						video_id = urlparse.parse_qs(urlparse.urlparse(input).query)['v'][0]
					except:
						return "Sorry " + username + ", that URL does not appear to have a YouTube video in it FeelsBadMan :gun:"
				else:
					video_id = input
				try:				
					video = pafy.new("https://www.youtube.com/watch?v=" + video_id)
				except ValueError:
					query = ""
					for i in range(1, len(command_args)):
						query += command_args[i]
					query_string = urlparse.urlencode({"search_query" : query})
					html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
					search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
					try:
						video = pafy.new("https://www.youtube.com/watch?v=" + search_results[0])
					except ValueError:
						return "Something horrible happened when I tried loading your video!"
				if video is None:
					return "Whoops! An error occurred upon processing the video!"
				if video.length > 600:
					return "Sorry " + username + ", the song must be less than 10 minutes long FeelsBadMan :gun:"
				if self.is_song_in_queue(video_id):
					return "Sorry " + username + ", the song is already in the queue NotLikeThis"

				audio_streams = video.audiostreams
				desired_stream = None
				for a in audio_streams:
					print(a.extension)
						desired_stream = a

				if desired_stream == None:
					return "No compatible format found for the song " + username + " FeelsBadMan :gun:" 

				if not os.path.isfile("tmp/" + video_id + "." + desired_stream.extension):
					desired_stream.download(filepath="tmp/" + video_id + "." + desired_stream.extension)

				# TODO: Check if file exists 
				event_overview.song_list.append({
					"username": username,
					"filename": "tmp/" + video_id + "." + desired_stream.extension,
					"title": video.title,
					"id": video_id,
					"length": video.length
				})

				return "Added the song '" + video.title + "' to the queue."

		if command_args[0] == "!songlist" or command_args[0] == "!sl":
			res = ""
			for i in range(0, min(3, len(event_overview.song_list))):
				res += "#" + str(i + 1) + ": " + event_overview.song_list[i]["title"]
			return res

	def is_song_in_queue(self, id):
		for i in range(0, len(event_overview.song_list)):
			if id == event_overview.song_list[i]["id"]:
				return True
		return False

	

