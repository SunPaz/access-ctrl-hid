"""
	IOEcho device, receive GPIO, send them thought TCP to target
"""

__all__ = ['IOEcho']
__version__ = '0.1'

from .deviceBase import DeviceBase
from time import sleep
import requests
import json

try:
	import RPi.GPIO as GPIO
	is_running_on_pi = True
except RuntimeError:
	print("Starting without GPIO")
	is_running_on_pi = False
	pass

class IOEcho(DeviceBase):
	pin_and_label_matrix = ''
	def __init__(self, name, pin_and_label_matrix):
		DeviceBase.__init__(self, name)
		DeviceBase.type = "IOEcho"
		if is_running_on_pi == True:
			print("Starting IOEcho device.")

			"""
				Set pin numbering mode
			"""
			GPIO.setmode(GPIO.BOARD)

			"""
				TODO : Add dynamic configuration, or stroe pin map in a file
			"""
			self.pin_and_label_matrix = [
				{'pin': 3, 'label': 'S011', 'value': '0'},
				{'pin': 5, 'label': 'S012', 'value': '0'},
				{'pin': 7, 'label': 'S033', 'value': '0'},
				{'pin': 11, 'label': 'S021', 'value': '0'},
				{'pin': 13, 'label': 'S022', 'value': '0'},
				{'pin': 15, 'label': 'S023', 'value': '0'},
				{'pin': 19, 'label': 'S031', 'value': '0'},
				{'pin': 21, 'label': 'S032', 'value': '0'},
				{'pin': 23, 'label': 'S033', 'value': '0'}
			]

			for pin_and_label in self.pin_and_label_matrix:
				""" Should add a physical pull down """
				GPIO.setup(pin_and_label['pin'], GPIO.IN)
				GPIO.add_event_detect(pin_and_label['pin'], GPIO.RISING, callback=self._on_data_received)
				print("Pin " + str(pin_and_label['pin']) + " initialized as input.")

			print("IOEcho device built !")

	#Overrided from DeviceBase
	def main_loop(self):
		""" Starts RFID reading loop """
		try:
			print("Starting controller...")
			if is_running_on_pi == True:
				while self.must_stop == False :
					if self.is_zone_enabled == True:
						self.is_running = True
						""" Controller is enable, start reading """
						#Prevent over-header
						sleep(1)

					else:
						""" Controller is disable, wait for a valid configuration """
						break
		finally:
			print("Reading loop stopped")

		sleep(1)

	#Overrided from DeviceBase
	def get_status(self):
		for pin_and_label in self.pin_and_label_matrix:
			pin_and_label['value'] = GPIO.input(pin_and_label['pin'])

		return str(self.pin_and_label_matrix)

	def _on_data_received(self, gpio):
		if is_running_on_pi == True:
			try:
				""" Send GPIO signal to open the door """
				for pin_and_label in self.pin_and_label_matrix:
					if pin_and_label['pin'] == gpio:
						self.echo_signal_to_target(pin_and_label['label'])
						""" Sleep 500 ms, avoid bouncing """
						sleep(0.5)
						break
			except RuntimeError:
				pass

	def echo_signal_to_target(self, signal):
		print("Sending " + str(signal) + " signal to target")
		socket = socket(AF_INET, SOCK_DGRAM)
		socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		socket.sendto(bytes(str(signal).encode('utf-8')), ('192.168.2.188', 900))

	#Overrided from DeviceBase
	def stop_loop(self):
		if is_running_on_pi == True:
			GPIO.cleanup()

		self.must_stop = True
