#DB.py is responsible for database operations. Mainly storing minutes and activities
import sqlite3

db = sqlite3.connect('db.db')
cur = db.cursor()



FIELDS_IN_ORDER = 'movecount, posaveragex, posaveragey, lefts, rights, mids, letters, numbers, whitespace, other, red, green, blue'

#todo implement posvariance and scrolls (currently default 0)
def setup():
	cur.execute('create table if not exists activities(id integer primary key autoincrement, name text unique, isdeleted integer default 0)')
	cur.execute('create table if not exists minutes(id text primary key, myguess integer default -1, correctanswer integer default -1, teachtime integer default -1,\
					movecount real, posaveragex real, posaveragey real, posvariance real default 0, lefts real, rights real, mids real, scrolls real default 0,\
					letters real, numbers real, whitespace real, other real,\
					red real, green real, blue real)')
	db.commit()

setup()

def addMinute(minuteIDName, data, myGuess):
	cur.execute('insert into minutes (id, '+FIELDS_IN_ORDER+', myguess)\
				values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (minuteIDName,)+data+(myGuess,))
	db.commit()

def getMinute(minuteIDName):
	cur.execute('select '+FIELDS_IN_ORDER+' from minutes where id = ?', (minuteIDName,))
	
	return cur.fetchone()

def getMarkedMinutes():
	cur.execute('select '+FIELDS_IN_ORDER+' from minutes where correctanswer != -1')
	a = cur.fetchall()
	
	cur.execute('select correctanswer from minutes where correctanswer != -1')
	b = cur.fetchall()
	
	return (a, b)

def addActivity(name):
	cur.execute("insert into activities (name) values (?)", (name, ))
	db.commit()


def actIDToName(id):
	if id == -1:
		return "Untrained MLP!"
	cur.execute("select name from activities where id = ?", (id,))
	return str(cur.fetchone()[0])

def listActivities():
	cur.execute("select id from activities")
	l = [x[0] for x in cur.fetchall()]
	return l

def setCorrectAnswer(minuteID, activityID, teachTime):
	cur.execute('update minutes set correctanswer = ?, teachTime = ? where id = ?', (activityID, teachTime, minuteID))
	db.commit()
