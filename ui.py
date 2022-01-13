from multiprocessing import Queue

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import PyQt5.QtCore as Qt

from db import addActivity, listActivityNames

label = None
queue = None
reverseQueue = None
b1 = None
b2 = None

def updateLabel():
	global b1, b2

	while not(queue.empty()):
		msg = queue.get()
		if len(msg) > 0 and msg[0] == '_':
			if msg == '_running True': b1.setText('Running')
			if msg == '_running False': b1.setText('Not Running')
			if msg == '_recording True': b2.setText('Recording')
			if msg == '_recording False': b2.setText('Not Recording')
		else:
			label.setText(msg)



def toggleRunning():
	global b1
	global reverseQueue

	#todo or (reverse button press)

	if b1.text() == 'Not Running':
		b1.setText('Starting Running')
	else:
		b1.setText('Stopping Running')

	reverseQueue.put('running')



dialogET = None
popup = None
def createNewActivity():
	global dialogET
	global popup
	cur = listActivityNames()
	dlg = QDialog()
	
	popup = dlg

	dialogET = QLineEdit(dlg)
	btn = QPushButton('Ok', dlg)
	btn2 = QPushButton('Cancel', dlg)
	btn.move(50,50)
	btn2.move(0,50)
	ql = QLabel('\n'.join(cur), dlg)
	ql.move(50, 100)


	btn.clicked.connect(finishCreatingNew)
	btn2.clicked.connect(closePopup)


	dlg.resize(120, 400)

	dlg.exec_()

	# dlg.setWindowModality(Qt.ApplicationModal)

def finishCreatingNew():
	global dialogET
	name = dialogET.text()
	addActivity(name)
	closePopup()

def closePopup():
	global popup
	popup.close()


def toggleRecording():
	global b2
	global reverseQueue


	if b2.text() == 'Not Recording':
		b2.setText('Starting Recording')
	else:
		b2.setText('Stopping Recording')

	reverseQueue.put('recording')

def normalQuit():
	global app
	global reverseQueue

	reverseQueue.put('exit')

	app.quit()

app = None

def setupUI(q, reverseQ):
	global label
	global queue
	global reverseQueue
	global b1, b2
	global app

	queue = q
	reverseQueue = reverseQ


	app = QApplication([])
	window = QWidget()
	_layout = QHBoxLayout()
	layout1 = QVBoxLayout()
	layout2 = QVBoxLayout()
	layout3 = QHBoxLayout()

	b1 = QPushButton("Not Running")
	b1.clicked.connect(toggleRunning)
	b2 = QPushButton("Not Recording")
	b2.clicked.connect(toggleRecording)


	layout1.addWidget(b1)
	layout1.addWidget(b2)
	label = QLabel("Hi")
	font = label.font()
	font.setPointSize(20)
	label.setFont(font)
	label.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); color: #FF007F; }")


	layout2.addWidget(label)


	#Make main window transparent
	window.setAttribute(Qt.WA_TranslucentBackground, True)
	window.setAttribute(Qt.WA_NoSystemBackground, True)
	window.setWindowFlags(Qt.FramelessWindowHint)
	window.move(0,100)

	bb1 = QPushButton("Add")
	bb2 = QPushButton("Teach")
	bb3 = QPushButton("Quit")

	bb1.setMaximumWidth(40)
	bb2.setMaximumWidth(40)
	bb3.setMaximumWidth(40)

	bb1.clicked.connect(createNewActivity)
	bb3.clicked.connect(normalQuit)

	layout3.addWidget(bb1)
	layout3.addWidget(bb2)
	layout3.addWidget(bb3)

	layout1.addLayout(layout3)

	_layout.addLayout(layout1)
	_layout.addLayout(layout2)
	window.setLayout(_layout)
	window.show()

	timer = QTimer()
	timer.timeout.connect(updateLabel)
	timer.start(100)


	app.exec_()

	window=0
