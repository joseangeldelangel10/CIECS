"""
----------------------------------- Python module to generate an mp3 player -------------------------------  
Developed by:
      - Leonardo Javier Nava Castellanos        ITESM CEM       A01750595
      - Jose Angel Del Angel Dominguez          ITESM CEM       A01749386

The following program is aimed to serve a multitouch graphic interface that runs in a RaspberryPi 4 - B and helps such
interface to create an instance of an mp3 player [PMP3] that along with pygame stores and reproduces a reproduction 
queue, in addition this mp3 player also performs basic reproduction controls such as playing/pausing a song, playing
the next song in the queue, and playing the last song in the queue.
 
For further technical details check the report at 
https://drive.google.com/drive/folders/1hk3mURtGdiiILylYTYTO4d61Ju5Ksm_t?usp=sharing
 
"""
import pygame as pg
import time

class PMP3():
	"""docstring for PMP3"""
	def __init__(self):
		super(PMP3, self).__init__()
		self.reproducing = False
		self.paused = True
		self.mixer = pg.mixer
		self.mixer.init(44100, -16, 2, 2048)
		self.queue = []
		self.i = 0

	def start_playing(self, song = ""):
		if not self.reproducing: 
			self.mixer.music.load(song)
			self.mixer.music.play()
			self.reproducing = True
			self.paused = False
		else:
			self.mixer.music.stop()
			self.mixer.music.load(song)
			self.mixer.music.play()
			self.reproducing = True
			self.paused = False

	def play_pause(self):
		if self.reproducing and not self.paused:
			self.mixer.music.pause()
			self.paused = True
		elif self.reproducing and self.paused:
			self.mixer.music.unpause()
			self.paused = False

	def Rewind(self):
		if( self.i -1 >= 0 ):
			self.start_playing(self.queue[self.i - 1])
			self.paused = False
			self.i -= 1
		else:
			return 0
		return -1
		

	def Forward(self):
		try:
			self.start_playing(self.queue[self.i +1])
			self.i += 1
			self.paused = False
		except IndexError:
			return 0
		return 1


	def check_status(self):
		if self.mixer.music.get_busy() == 0:
			return self.Forward()
		else:
			return 0
			
