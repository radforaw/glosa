import csv
import json
import datetime
import calendar
import shelve
import io
import time
import cPickle as pickle
import zipfile
import itertools
from math import atan2,pi,sqrt
from multiprocessing import Pool
from multiimport import *
from collections import defaultdict
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import codecs

from geometryfunc import *
import linestuff
#import OSMmap
import sqlite3

def csvimporter(filename='files/GLOSA2.csv'):
	'''load a csv file. Converts datetimes to 'epoch' timestamp and processes the Time offset.
	Converts timestamp to lat lon.
	return a dictionary with keys being Vehicle ID's and value being a list of the key attributes.
	'''
	with zipfile.ZipFile(filename,'r') as zfile:
		unzipped= zfile.namelist()[0]
		
		
		#result=u"VehicleId,createdAt,Longitude,Latitude,DeviceTime,TimeOffset,IntersectionId,Event,Distance,RouteId,Speed,CalculationAdvisory,SPAT,Heading,MAP,Lane,AdvisoryEnabled\n"
		result=zfile.read(unzipped).encode("utf-8-sig")
		result=result.encode("ascii","ignore")
		#result=zfile.read(unzipped).encode("utf-8-sig")
	print result[:400]

	p=Pool(4)
	d=[a for a in p.map(impfunc,[n for n in csv.DictReader(result.splitlines())])]
	p.close()
	p.join()

	v=defaultdict(list)
	for n in d:
		v[n[0]].append(n[1])
	v={k:v[k] for k in v if len(v[k])>2}
	for n in v:
		print n,len(v[n])
	return v

def journeysort(v,routes): #inbound,outbound):
	'''
	take the processed journey dictionary, and return just journeys that are on the selected route / routes
	v is the dictionary of processed GPS points
	inbound / outbound are lists of points representing the inbound / outbound journeys to be compared
	'''
	p=Pool(4)
	d=[j for j in p.map(addfunc,[(v[n],n,routes) for n in v])] # n is the driver
	p.close()
	p.join()
	lon=[]
	jnum=0
	res={}
	for n in d:
		for q in n: #(q=name of leg)
			res[q]={}
			for y in n[q]:
				#print 'n', n,'q',q
				res[q][y]=createjourneys(n[q][y])
				for a in res[q][y]: #(a:name of driver)
					print a,len(res[q][y][a])
					if len(res[q][y][a])>10:
						lon.append([[y,q,jnum, res[q][y][a][0][6]]+t for t in res[q][y][a]])
						jnum+=1
	return lon
	
def createjourneys(journeylist):
	'''
	Split into journeys, by making sure that they are 300 seconds apart
	'''
	result={}
	journey=1
	try:
		last=journeylist[0][6] # try block here
	except:
		journey=0
		last=0
	for a in journeylist:
		if -300>a[6]-last or a[6]-last>300:
			journey+=1
		try:
			result[journey].append(a)
		except:
			result[journey]=[]
			result[journey].append(a)
		last=a[6]
	return result

class mysql():
	def __init__(self,name=":memory:"):
		self.conn=sqlite3.connect(name)
		self.c=self.conn.cursor()
		
	def __del__(self):
		self.conn.close()

	#d INTEGER PRIMARY KEY AUTOINCREMENT
	
	def createmaintable(self):
		self.c.execute('''CREATE TABLE main ( driver TEXT, route TEXT, journey INT,startime REAL, angle REAL,distfromlast REAL,speed REAL,secsfromlast INT,easting REAL, northing REAL, epochtime REAL, lightcol TEXT, secstillchange INT)''')
		self.conn.commit()
		
	def addmainrecord(self,data):
		self.c.executemany('INSERT INTO main VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',data)
		self.conn.commit()
		
	def getdrivers(self):
		print [x for x in self.c.execute('SELECT driver,COUNT(DISTINCT journey) FROM main GROUP BY driver')]
	
	def getdriverroutes(self,driver):
		for n in [x for x in self.c.execute('''SELECT * FROM main WHERE driver=? ''',(driver,))]:
			print n
	
	def getjourney(self):
		print [x for x in self.c.execute('SELECT driver,route,COUNT(DISTINCT route) FROM main GROUP BY journey')]
	


#csvimporter('data/GLOSA_Production_Eventlog_Export_201808031504.csv.zip.py')
#outbound=linestuff.routecalc("data/route.csv",10)
#inbound=linestuff.routecalc("data/routeback.csv",10)
routes={"Outbound":linestuff.simpleline("data/route.csv"),
	"Inbound":linestuff.simpleline("data/routeback.csv"),
	"Tyburn Inbound":linestuff.simpleline("data/ti.txt"),
	"Tyburn Outbound":linestuff.simpleline("data/to.txt")}

j=csvimporter('data/GLOSA_Production_Eventlog_Export_20190220.csv.zip')
tmp=journeysort(j,routes)
x=mysql()
x.createmaintable()
i=0
for a in tmp:
	print i
	x.addmainrecord(a)
	i+=1

x.getdrivers()
#x.getdriverroutes("Matt Phone")
x.getjourney()
