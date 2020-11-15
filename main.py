#Main.py is the main thread responsible for launching the other threads and communicating between them
from datetime import datetime
import multiprocessing
from time import sleep
if __name__ == "__main__":
	from ui import setupUI
	from datalayer import processMeasurementData

from keylogger import proc_m, proc_k
from screenshot import screenshot, finalizeScreenshot

#Simple function to get current minute as a unique string
def getMinuteID():
	return datetime.now().strftime("%Y_%m_%d_%H_%M")

def message(s):
	print(s)



#Necessary for multiprocessing
if __name__ == "__main__":

	STATE_RUNNING = False #If measurements are being made
	STATE_RECORDING = False #Only relevant when running, takes screenshots to assist manual teaching and marks data for learning
	
	keyloggerQueue = multiprocessing.Queue() #Measuring processes write to this
	
	uioutq = multiprocessing.Queue() #UI out queue
	uiinq = multiprocessing.Queue() #UI in queue
	
	message('starting subprocesses')
	
	#Mouse process
	pm = multiprocessing.Process(target=proc_m, args = (keyloggerQueue,))
	pm.start()
	
	#Keyboard process
	pk = multiprocessing.Process(target=proc_k, args = (keyloggerQueue,))
	pk.start()
	
	#UI
	ui = multiprocessing.Process(target=setupUI, args = (uioutq, uiinq))
	ui.start()
	
	message('program ready')
	
	#Starting time
	curMin = datetime.now().minute	
	#Note: the program only measures full minutes. Therefore the minute it is started is always ignored.
	
	while True: #Each real time minute is one loop iteration
		
		#If running: a screenshot is taken at :30 for color data
		#If also recording: two additional screenshots taken at :15 and :45 for identification
		screenshots = [None, None, None]
		
		#We only save screenshots in recording mode
		minuteIDName = getMinuteID()
		
		#Processing happens at the end of minute
		while datetime.now().minute == curMin:
			
			sec = datetime.now().second
			
			if STATE_RUNNING and STATE_RECORDING and screenshots[0] == None and sec >= 15:
				screenshots[0] = screenshot(0)
			
			if STATE_RUNNING and screenshots[1] == None and sec >= 30:
				screenshots[1] = screenshot(1)
			
			if STATE_RUNNING and STATE_RECORDING and screenshots[2] == None and sec >= 45:
				screenshots[2] = screenshot(2)
			
			
			sleep(1) #Not sleeping for entire minutes makes sure computing time doesn't introduce a delay

		#Exiting inner while loop means end of the minute, handle everything
		#Note: computational delay doesn't cause problems because measurement is on a separate thread
		
		#Collect measured data
		#Note: if not running, this empties queue
		data = []
		while not(keyloggerQueue.empty()):
			msg = keyloggerQueue.get()
			data += [msg]
		
		
		if STATE_RUNNING:
			dominantColor = finalizeScreenshot(minuteIDName if STATE_RECORDING else None)
			
			text = processMeasurementData(data, dominantColor)
			uioutq.put(str(text))
			print(text)
		
			#todo send data to database
	
	
	
		#todo don't save minute when we stopped running/recording?
		while not(uiinq.empty()):
			msg = uiinq.get()
			if msg == 'running':
				STATE_RUNNING = not(STATE_RUNNING)
			elif msg == 'recording':
				STATE_RECORDING = not(STATE_RECORDING)
		
		uioutq.put(f'_running {str(STATE_RUNNING)}')
		uioutq.put(f'_recording {str(STATE_RECORDING)}')
		
		
		curMin = datetime.now().minute	

	#Kill children
	pm.terminate()
	pk.terminate()
	
	pm.join()
	pk.join()
	
	#todo also kill ui
	
	message("end")


































