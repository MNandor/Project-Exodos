#Datalayer.py converts incoming data into a format that can be stored or used in the MLP
from math import tanh
from statistics import mean

def processMeasurementData(data, dominantColor):
	mouseData = [0,0,0,0] # Click, RightClick, Middle, Scroll
	kbData = [0,0,0,0] # Letters, Numbers, Whitespace, Other
	mouseMovement = [] #Each movement (math done later)
	
	
	movC = 0
	cliC = 0
	preC = 0
	
	for i in data:
		if i[0] == "M":
			coords = i.split(" ")[1:]
			coords = [int(x) for x in coords]
			mouseMovement += [coords]
		if i[0] == "C":
			w = i.split(" ")[1]
			if w == "Button.left": mouseData[0] += 1
			if w == "Button.right": mouseData[1] += 1
			if w == "Button.middle": mouseData[2] += 1
		if i[0] == "K":
			w = i.split(" ")[1]
			if "'" in w:
				w = w.replace("'", "")
				if w.isalpha(): kbData[0] += 1
				elif w.isnumeric(): kbData[1] += 1 #todo else other
			elif w in ["Key.tab", "Key.space", "Key.enter"]:	
				kbData[2] += 1
			else:
				kbData[3] += 1
	
	#If we had no mouse movement, we can't calculate mean. Hardcode an average-ish value
	if len(mouseMovement) == 0:
		mouseMovement += [(500, 500)]
		
	
	#All numbers are converted into values between 0 and 1
	#Hyperbolic tangent (tanh) helps convert unbounded numbers
	mData = (
		tanh(len(mouseMovement)/5000), #Movement frequency
		tanh(mean([x[0] for x in mouseMovement])/1920), #X coordinate of mouse
		tanh(mean([y[1] for y in mouseMovement])/1024), #Y coordinate
		
		tanh(mouseData[0]/200), #Left click frequency
		tanh(mouseData[1]/200), #Right click
		tanh(mouseData[2]/200), #Middle
		
		tanh(kbData[0]/400), #Letter keypress frequency
		tanh(kbData[1]/400), #Numerical
		tanh(kbData[2]/400), #Whitespace
		tanh(kbData[3]/400), #Other
		
		#Note: these are already bounded
		dominantColor[0]/256, #Red
		dominantColor[1]/256, #Green
		dominantColor[2]/256 #Blue
	)
	
	return mData
	
	'''
	def addMinute(time, screenColors, mouseData, kbData, mouseMovement, screenshotTaken):
	cur.execute("insert into minutesmeta (id) values (?)", (time,))

	cur.execute("insert into minutesmouse (id, movecount, posaveragex, posaveragey, lefts, rights, mids) values (?,?,?,?,?,?,?)",
	(time, len(mouseMovement), mean([x[0] for x in mouseMovement]), mean([x[1] for x in mouseMovement]), mouseData[0], mouseData[1], mouseData[2]))
	cur.execute("insert into minuteskeyboard (id, letters, numbers, whitespace, other) values (?,?,?,?,?)",
	tuple([time]+kbData))
	cur.execute("insert into minutesscreen (id, red, green, blue) values (?,?,?,?)",
	tuple([time]+list(screenColors)))
	
	db.commit()
	
	'''
	'''
	addMinute(time, screenColors, mouseData, kbData, mouseMovement, recordModeEh)
	
	formatted = _getCurData(time)[0]
	
	id = classifier.answerThis(formatted)[0]
	print(id)
	
	storeMyGuess(time, id)
	
	return actIDToName(int(id))
	'''
