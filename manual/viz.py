import sqlite3
import pandas as pd
from math import tanh
import matplotlib.pyplot as plt


db = sqlite3.connect('db.db')

df = pd.read_sql_query("SELECT * FROM minutesmeta\
	left join minutesmouse on minutesmeta.id = minutesmouse.id\
	left join minuteskeyboard on minutesmeta.id = minuteskeyboard.id\
	left join minutesscreen on minutesmeta.id = minutesscreen.id\
	where minutesmeta.id > \"2020_06_15_11_59\"\
	and minutesmeta.id < \"2020_06_15_15_59\"\
	order by minutesmeta.id", db)

df = df.loc[:,~df.columns.duplicated()]

df["movecount"] = df["movecount"].apply(lambda x: tanh(x/5000))
df["letters"] = df["letters"].apply(lambda x: tanh(x/400))
df["lefts"] = df["lefts"].apply(lambda x: tanh(x/200))
df["brightness"] = df["red"]+df["green"]+df["blue"]
df["id"] = df["id"].apply(lambda x: int(x[-5:].split("_")[0])*60+int(x[-5:].split("_")[1]))

df["one"] = df["id"].apply(lambda x: 1)
df["two"] = df["id"].apply(lambda x: 2)


ax = df.plot.scatter(x = "one", y = "id", c = "correctanswer", colormap = "hsv")
df.plot.scatter(x = "two", y = "id", c = "myguess", colormap = "hsv", ax = ax)
plt.show()


exit()
for c1 in df.columns:
	for c2 in df.columns:
		bads = ["teachtime", "correctanswer", "myguess", "posvariance", "scrolls", "rights", "mids", "red", "green", "blue", "numbers", "whitespace"]
		if c1 in bads or c2 in bads: continue
		if c1 == c2: continue
		ax = df.plot.scatter(x = c1, y = c2, c = "correctanswer", colormap = "hsv")
		plt.show()
