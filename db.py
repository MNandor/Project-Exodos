#DB.py is responsible for database operations. Mainly storing minutes and activities
import sqlite3

db = sqlite3.connect('db.db')
cur = db.cursor()

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
	cur.execute('insert into minutes (id, movecount, posaveragex, posaveragey, lefts, rights, mids, letters, numbers, whitespace, other, red, green, blue, myguess)\
				values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (minuteIDName,)+data+(myGuess,))
	db.commit()

def getMinute(minuteIDName):
	cur.execute('select movecount, posaveragex, posaveragey, lefts, rights, mids, letters, numbers, whitespace, other, red, green, blue\
	from minutes where id = ?', (minuteIDName,))
	
	return cur.fetchone()


def addActivity(name):
	cur.execute("insert into activities (name) values (?)", (name, ))
	db.commit()


def actIDToName(id):
	if id == -1:
		return "Untrained MLP!"
	cur.execute("select name from activities where id = ?", (id,))
	return str(cur.fetchone()[0])
