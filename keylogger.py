#Two subprocesses log keyboard and mouse usage
from pynput.mouse import Listener as ML
from pynput.keyboard import Listener as KL

queue = None

#Todo consider logging position at regular intervals instead of when mouse is moved
def mouseMove(x, y):
	queue.put(f"M {x} {y}")


def mouseClick(x, y, button, pressed):
	if pressed:
		queue.put(f"C {button}")

def keyPress(key):
	queue.put(f"K {key}")
	

def proc_k(q):
	global queue
	queue = q
	
	with KL(on_press=keyPress) as listener:
		listener.join()


def proc_m(q):	
	global queue
	queue = q
	
	with ML(on_move=mouseMove, on_click=mouseClick) as listener:
		listener.join()
