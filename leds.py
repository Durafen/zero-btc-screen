import os

class Leds:
	status = True
	
#	def __init__(self):
#		self.off();
	
	
	def off(self):
		if self.status == True:
			os.system("sudo bash -c \"echo none > /sys/class/leds/led1/trigger\"")
			self.status = False
		
	def on(self):
		if self.status == False:
			os.system("sudo bash -c \"echo default-on > /sys/class/leds/led1/trigger\"")
			self.status = True
			
	
