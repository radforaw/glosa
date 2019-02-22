import sqlite3
import os
print 'thing'+os.getcwd()
class mysql():
	def __init__(self,name="mydata/database/glosadatabase.db"):
		self.conn=sqlite3.connect(name)
		self.c=self.conn.cursor()
		
	def __del__(self):
		self.conn.close()
	
	def createmaintable(self):
		self.c.execute('''CREATE TABLE main ( driver TEXT, route TEXT, journey INT,startime REAL, angle REAL,distfromlast REAL,speed REAL,secsfromlast INT,easting REAL, northing REAL, epochtime REAL, lightcol TEXT, secstillchange INT)''')
		self.conn.commit()
		
	def addmainrecord(self,data):
		self.c.executemany('INSERT INTO main VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',data)
		self.conn.commit()
		
	def getdrivers(self):
		return [x for x in self.c.execute('SELECT driver,COUNT(DISTINCT journey) FROM main GROUP BY driver')]
	
	def getdriverroutes(self,driver):
		return [x for x in self.c.execute('''SELECT route,COUNT(DISTINCT journey) FROM main WHERE driver=? GROUP BY route''',(driver,))]

	def getdriverroutesjourney(self,driver,route):
		print driver,route
		return [x for x in self.c.execute('''SELECT journey,startime FROM main WHERE route=? AND driver=? GROUP BY startime''',(route,driver,))]
	
	def getmapdata(self,journey):
		return [x for x in self.c.execute('''SELECT easting,northing,lightcol,epochtime,speed FROM main WHERE journey=?''',(journey,))]

	


