import sqlite3
import os
import time
from shutil import rmtree
import classifier


db = sqlite3.connect('db.db')
cur = db.cursor()



def getMinutes():
	cur.execute("select * from minutesmeta\
	left join minutesmouse on minutesmeta.id = minutesmouse.id\
	left join minuteskeyboard on minutesmeta.id = minuteskeyboard.id\
	left join minutesscreen on minutesmeta.id = minutesscreen.id")
	
	ar = cur.fetchall()
	for a in ar:
		print(a)

def storeMyGuess(time, activity):
	cur.execute("update minutesmeta set myguess = ? where id = ?", (int(activity), time))
	db.commit()

'''
def addMinute(time, screenColors, mouseData, kbData, mouseMovement, screenshotTaken):
	cur.execute("insert into minutesmeta (id) values (?)", (time,))
	if len(mouseMovement) == 0:
		mouseMovement += [(500, 500)] #mean error
	cur.execute("insert into minutesmouse (id, movecount, posaveragex, posaveragey, lefts, rights, mids) values (?,?,?,?,?,?,?)",
	(time, len(mouseMovement), mean([x[0] for x in mouseMovement]), mean([x[1] for x in mouseMovement]), mouseData[0], mouseData[1], mouseData[2]))
	cur.execute("insert into minuteskeyboard (id, letters, numbers, whitespace, other) values (?,?,?,?,?)",
	tuple([time]+kbData))
	cur.execute("insert into minutesscreen (id, red, green, blue) values (?,?,?,?)",
	tuple([time]+list(screenColors)))
	
	db.commit()
'''
	


def setup():
	cur.execute("create table if not exists activities(id integer primary key autoincrement, name text unique, isdeleted integer default 0)")
	cur.execute("create table if not exists minutesmeta(id text primary key, myguess integer default 0, correctanswer integer default -1, teachtime integer default -1)")
	cur.execute("create table if not exists minutesmouse(id text primary key, movecount integer, posaveragex real, posaveragey real, posvariance real, lefts integer, rights integer, mids integer, scrolls integer default 0)")
	cur.execute("create table if not exists minuteskeyboard(id text primary key, letters integer, numbers integer, whitespace integer, other integer)")
	cur.execute("create table if not exists minutesscreen(id text primary key, red integer, green integer, blue integer)")
	
	db.commit()


def addActivity(name):
	cur.execute("insert into activities (name) values (?)", (name, ))
	db.commit()

def listActivities():
	cur.execute("select name from activities")
	l = [x[0] for x in cur.fetchall()]
	return l

def actNameToID(name):
	cur.execute("select id from activities where name = ?", (name, ))
	return cur.fetchone()[0]

def actIDToName(id):
	cur.execute("select name from activities where id = ?", (id,))
	return cur.fetchone()[0]


def teach():
	l = listActivities()
	for a in l:
		os.mkdir("screenshots/"+a)
	
	print("Move each screenshot into the right folder or delete them if unsure")
	os.startfile("screenshots")
	
	input("Press enter when done")
	
	teachtime = int(time.time())
	
	corrects = []
	
	for a in l:
		ml = os.listdir("screenshots/"+a)
		ml = [x.replace(".png", "") for x in ml]
		print(ml)
		
		actID = actNameToID(a)
		
		for m in ml:
			wasCorrect = teachDB(m, actID, teachtime)
			corrects += [wasCorrect]
		
		rmtree("screenshots/"+a)
	
	corrects = [x for x in corrects if x != None]
	print(corrects)
	print(f"I was {corrects.count(True)/len(corrects)*100}% correct!")
	
	db.commit()

def teachDB(id, answer, teachTime):
	cur.execute("select myguess from minutesmeta where id = ?", (id, ))
	try:
		guess = cur.fetchone()[0]
	except TypeError:
		return None
	cur.execute("update minutesmeta set correctanswer = ?, teachTime = ? where id = ?", (answer, teachTime, id))
	
	print(">>>", answer, guess)
	
	return answer == guess


def learn():
	
	
	l = _getCurData("")
	
	classifier.learnThese(l)

def _getCurData(id):
	selector = " where minutesmeta.id = \""+str(id)+"\""
	
	if id == "":
		selector = " where correctanswer != -1"
	
	cur.execute("select minutesmeta.id, correctanswer, movecount, posaveragex, posaveragey, lefts, rights, mids, letters, numbers, whitespace, other, red, green, blue\
	from minutesmeta\
	left join minutesmouse on minutesmeta.id = minutesmouse.id\
	left join minuteskeyboard on minutesmeta.id = minuteskeyboard.id\
	left join minutesscreen on minutesmeta.id = minutesscreen.id" + selector)
	
	l = cur.fetchall()
	l = [((x[0], x[1]), tuple(x[2:])) for x in l]
	return l
		

def ui():
	while True:
		print("0: setup\n1: getMinutes\n2: getActivities\n3: addActivity\n4: teach\n5: learn")
		num = int(input())
		
		if num == 0: print( setup() )
		if num == 1: print( getMinutes() )
		if num == 2: print( listActivities() )
		if num == 3: print( addActivity(input()) )
		if num == 4: print( teach() )
		if num == 5: print( learn() )
	


setup()
