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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from geometryfunc import *
import linestuff

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
		print s1,s2
	else:
		s1="Grey"
		s2=-1
	return [tn,[t,l[0],l[1],n['Speed'],n['CalculationAdvisory'],s1,s2]]
