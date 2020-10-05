from datetime import datetime
import multiprocessing
from time import sleep
from screenshot import screenshot
from keylogger import *
if __name__ == "__main__":
	from ui import setupUI
	from db import sendData


def getMinuteID():
	return datetime.now().strftime("%Y_%m_%d_%H_%M")


#Main Process handles data coming from two subprocesses in a Queue



if __name__ == "__main__":
	
	running = True
	takeScreenshots = True

	queue = multiprocessing.Queue()
	
	uioutq = multiprocessing.Queue() #ui out queue
	uiinq = multiprocessing.Queue() #ui in queue
	
	print("starting")
	
	#Mouse process
	pm = multiprocessing.Process(target=proc_m, args = (queue,))
	pm.start()
	
	#Keyboard process
	pk = multiprocessing.Process(target=proc_k, args = (queue,))
	pk.start()
	
	#UI
	ui = multiprocessing.Process(target=setupUI, args = (uioutq, uiinq))
	ui.start()
	
	print("waiting")
	
	#Starting time
	curMin = datetime.now().minute
	
	
	#Note: Since starting minute is not full, it is not measured
	if True:
		#Wait for minute start
		while datetime.now().minute == curMin:
			sleep(1)
		#Empty queue
		while not(queue.empty()):
			msg = queue.get()

	curMin = datetime.now().minute
	print("running")

	while running:
		hitMiddle = False
		print(f"Starting {getMinuteID()}")
		
		screenData = None
		minID = getMinuteID()
		data = []
		
		
		#Sleep seconds to compensate for computing time skew
		while datetime.now().minute == curMin:
			sleep(1)
			
			
			
			#Take screenshot
			if not(hitMiddle) and datetime.now().second >= 30:
				hitMiddle = True
				screenData = screenshot(getMinuteID(), takeScreenshots)
				
		
		curMin = datetime.now().minute
		
		
		while not(uiinq.empty()):
			uiinq.get()
		
		#Handle all keylogs
		while not(queue.empty()):
			msg = queue.get()
			data += [msg]
		
		text = sendData(minID, data, screenData, takeScreenshots)
		uioutq.put(text)
		print(text)
		
		
		
	
	#Kill children
	pm.terminate()
	pk.terminate()
	
	pm.join()
	pk.join()
	
	print("end")