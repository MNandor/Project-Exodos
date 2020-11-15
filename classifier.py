from sklearn.neural_network import MLPClassifier
import joblib
from statistics import mean


mylittlepony = None
try:
	mylittlepony = joblib.load("model.joblib")
	print("MLP loaded")
except FileNotFoundError:
	print("MLP started")
	mylittlepony = MLPClassifier(random_state=1, max_iter=700)


def learnThese(trainingData, trainingAnswers, testingSet, testingAnswers):
		
	mylittlepony.fit(trainingData, trainingAnswers)
	
	print("Done learning")
	
	if False:
		testPredictions = mylittlepony.predict(testingSet)
		
		print('Testing: ', mean([1 if testPredictions[i] == testingAnswers[i] else 0]))
	
	joblib.dump(mylittlepony, "model.joblib")

def answerThis(data):
	try:
		#print(str(mylittlepony.predict_proba( [data] )))
		return int(mylittlepony.predict([data])[0])
	except:
		return -1 #untrained model

