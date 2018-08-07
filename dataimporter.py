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
reload(sys)
sys.setdefaultencoding('utf-8')

from geometryfunc import *
import linestuff
#import OSMmap

def csvimporter(filename='files/GLOSA2.csv'):
	'''load a csv file. Converts datetimes to 'epoch' timestamp and processes the Time offset.
	Converts timestamp to lat lon.
	return a dictionary with keys being Vehicle ID's and value being a list of the key attributes.
	'''
	with zipfile.ZipFile(filename,'r') as zfile:
		unzipped= zfile.namelist()[0]
		result=u"VehicleId,createdAt,Longitude,Latitude,DeviceTime,TimeOffset,IntersectionId,Event,Distance,RouteId,Speed,CalculationAdvisory,SPAT,Heading,MAP,Lane,AdvisoryEnabled\n"

		result+=zfile.read(unzipped).encode("utf-8-sig")
	print result[:200]
	#with io.open(result, "r", encoding="utf-8-sig") as csvfile:
	csvfile=result.encode("utf-8-sig")
	del result
	print csvfile[:200]
	p=Pool(4)
	d=[a for a in p.map(impfunc,[n for n in csv.DictReader(io.StringIO(csvfile.decode("utf-8-sig")))])]
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
	res={}
	for n in d:
		for q in n:
			res[q]={}
			for y in n[q]:
				print 'here', q,y
				res[q][y]=createjourneys(n[q][y])
				for a in res[q][y]:
					print a,len(res[q][y][a])
	return res
	
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

	
	
#csvimporter('data/GLOSA_Production_Eventlog_Export_201808031504.csv.zip.py')
#outbound=linestuff.routecalc("data/route.csv",10)
#inbound=linestuff.routecalc("data/routeback.csv",10)
routes={"Outbound":linestuff.simpleline("data/route.csv"),"Inbound":linestuff.simpleline("data/routeback.csv")}

j=csvimporter('data/GLOSA_Production_Eventlog_Export_201808031504.csv.zip.py')
tmp=journeysort(j,routes)
