from multiprocessing import Queue

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import PyQt5.QtCore as Qt

label = None
queue = None
reverseQueue = None

def updateLabel():
	while not(queue.empty()):
		msg = queue.get()
		label.setText(msg)
	


def setupUI(q, reverseQ):
	global label
	global queue
	global reverseQueue
	queue = q
	reverseQueue = reverseQ
	
	
	app = QApplication([])
	window = QWidget()
	_layout = QHBoxLayout()
	layout1 = QVBoxLayout()
	layout2 = QVBoxLayout()

	b1 = QPushButton("Run")
	b2 = QPushButton("Teach")


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

	_layout.addLayout(layout1)
	_layout.addLayout(layout2)
	window.setLayout(_layout)
	window.show()
	
	timer = QTimer()
	timer.timeout.connect(updateLabel)
	timer.start(100)
	
	
	app.exec_()

	window=0
