import csv
import datetime
import calendar
from math import atan2,pi,sqrt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from geometryfunc import *

def impfunc(n):
	tmp=n['createdAt'][:-7] #Datetimes are in a funny format - this is a cludge to make it work
	t=datetime.datetime.strptime(tmp,'%Y-%m-%d %H:%M:%S.%f')
	l=WGS84toOSGB36(float(n['Latitude']),float(n['Longitude']))
	t= float(calendar.timegm(t.timetuple()))+ float(n['TimeOffset'])/1000
	tn=str(n['VehicleId'])
	#if tn not in v:
	#	v[tn]=[]
	s=n['SPAT']
	if s<>"NULL":
		s=s[s.find("(")+1:s.find(")")].split(" | ")
		s1=s[0]
		try:
			s2=int(s[1][s[1].find(": ")+2:])
		except IndexError:
			s2=-1
	else:
		s1="Grey"
		s2=-1
	return [tn,[t,l[0],l[1],n['Speed'],n['CalculationAdvisory'],s1,s2]]

def addfunc(f):
	a=f[0]
	n=f[1]
	routes=f[2]
	endresult=[]
	for b in range(len(routes)):
		endresult.append({})     # creates a dictionary for each direction (or route)
	a=sorted(a)
	last=(a[0][1],a[0][2])
	print len(a),n,
	old=angle(last,(a[1][1],a[1][2]))
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
		old=fin
		last=(result[1],result[2])
		prev=result[0]
	return endresult
