from sklearn.neural_network import MLPClassifier
from math import tanh
import joblib

mylittlepony = None
try:
	mylittlepony = joblib.load("model.joblib")
	print("MLP loaded")
except FileNotFoundError:
	print("MLP started")
	mylittlepony = MLPClassifier(random_state=1, max_iter=700)


def learnThese(l):
	
	
	
	l = [processData(line) for line in l]
	
	print("Learning from: ",len(l))
		
	mylittlepony.fit([x[1] for x in l], [x[0] for x in l])
	
	print("Done learning")
	
	joblib.dump(mylittlepony, "model.joblib")

def answerThis(line):
	line = processData(line)
	
	try:
		print(str(mylittlepony.predict_proba( [line[1]] )))
		return mylittlepony.predict( [line[1]] )
	except:
		return "No fit yet!"


def processData(line):
	print(line)
	# movecount, posaveragex, posaveragey, lefts, rights, mids, letters, numbers, whitespace, other, red, green, blue
	data = (line[0][1],
	(
		tanh(line[1][0]/5000),
		tanh(line[1][1]/1280),
		tanh(line[1][2]/1024),
		
		tanh(line[1][3]/200),
		tanh(line[1][4]/200),
		tanh(line[1][5]/200),
		
		tanh(line[1][6]/400),
		tanh(line[1][7]/400),
		tanh(line[1][8]/400),
		tanh(line[1][9]/400),
		
		tanh(line[1][10]/256),
		tanh(line[1][11]/256),
		tanh(line[1][12]/256)
	)
	)
	
	return data