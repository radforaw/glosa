import csv
import json
import datetime
import calendar
import shelve
import io
import time
import cPickle as pickle
import zipfile
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
	reader=csv.DictReader(io.StringIO(csvfile.decode("utf-8-sig")))
	v={}
	for n in reader:
		tmp=n['createdAt'][:-7] #Datetimes are in a funny format - this is a cludge to make it work
		t=datetime.datetime.strptime(tmp,'%Y-%m-%d %H:%M:%S.%f')
		l=WGS84toOSGB36(float(n['Latitude']),float(n['Longitude']))
		t= float(calendar.timegm(t.timetuple()))+ float(n['TimeOffset'])/1000
		tn=str(n['VehicleId'])
		if tn not in v:
			v[tn]=[]
		s=n['SPAT']
		if s<>"NULL":
			s=s[s.find("(")+1:s.find(")")].split(" | ")
			s1=s[0]
			try:
				s2=int(s[1][s[1].find(": ")+2:])
			except IndexError:
				s2=-1
			print s1,s2
		else:
			s1="Grey"
			s2=-1
		v[tn].append([t,l[0],l[1],n['Speed'],n['CalculationAdvisory'],s1,s2])
	return v


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
	return v


def journeysort(v,routes): #inbound,outbound):
	'''
	take the processed journey dictionary, and return just journeys that are on the selected route / routes
	v is the dictionary of processed GPS points
	inbound / outbound are lists of points representing the inbound / outbound journeys to be compared
	'''
	endresult=[]
	for a in range(len(routes)):
		endresult.append({})     # creates a dictionary for each direction (or route)
	for n in v: # n is the driver
		a=sorted(v[n])
		last=(a[0][1],a[0][2])
		print len(a),n,
		try:
			old=angle(last,(a[1][1],a[1][2]))
		except:
			continue
		prev=a[0][0]-62
		print last,old,prev
		for t in range(len(routes)): # sets up a list for each driver by direction ready for GPS points...
			endresult[t][n]=[]
		for result in a:
			if result[0]-prev>60 or float(result[3])<5.0:   #slower than 8 mph
				fin=old
			else:
				fin=angle(last,(result[1],result[2]))
			cnt=0
			for route in routes:		
				if closething((result[1],result[2]),fin,route):
					endresult[cnt][n].append([fin,dist(last,(result[1],result[2])), result[3],result[0]-prev,result[1],result[2],result[0],result[5],result[6]])
				cnt+=1
			try:
				print endresult[cnt][n][:-1]
			except:
				pass
			old=fin
			last=(result[1],result[2])
			prev=result[0]
	return endresult

def journeysort(v,routes): #inbound,outbound):
	'''
	take the processed journey dictionary, and return just journeys that are on the selected route / routes
	v is the dictionary of processed GPS points
	inbound / outbound are lists of points representing the inbound / outbound journeys to be compared
	'''
	p=Pool(4)
	d=[j for j in p.map(addfunc,[(v[n],n,routes) for n in v])] # n is the driver
	return d

def createjourneys(journeylist):
	'''
	Split into journeys, by making sure that they are 300 seconds apart
	'''
	result={}
	journey=[]
	for user in journeylist:
		journey=1
		try:
			last=journeylist[user][0][6] # try block here
		except:
			journey=0
			last=0
		for a in journeylist[user]:
			if -300>a[6]-last or a[6]-last>300:
				journey+=1
			try:
				result[(user,journey)].append(a)
			except:
				result[(user,journey)]=[]
				result[(user,journey)].append(a)
			last=a[6]
	return result

	
	
#csvimporter('data/GLOSA_Production_Eventlog_Export_201808031504.csv.zip.py')
outbound=linestuff.routecalc("data/route.csv",10)
inbound=linestuff.routecalc("data/routeback.csv",10)



j=csvimporter('data/GLOSA_Production_Eventlog_Export_201808031504.csv.zip.py')
#for n in j:
#	print n
#	print j[n]
t=shelve.open("journeys.s")
for x in journeysort(j,[outbound,inbound]):
	tmp=createjourneys(x)
	a=0
	for n in tmp:
		t[str[a]]=n
		a+=1
t.close()
