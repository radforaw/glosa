import math

def asline(points):
	'''point=list of points on polyline e.g. ((x1,y1),(x2,y2),(x3,y3))
	return startpoint, length and angle(as multipliers for x and y)'''
	newlineinfo=[]
	for n in range(len(points)-1):
		length=math.sqrt(((points[n][0]-points[n+1][0])**2)+((points[n][1]-points[n+1][1])**2))
		slope=math.atan2(float(points[n+1][0]-points[n][0]),float(points[n+1][1]-points[n][1]))
		ax,ay=math.sin(slope),math.cos(slope)
		newlineinfo.append([points[n],points[n+1],length,(ax,ay)])
	return newlineinfo
	
def distline(dist,line):
	'''return coordinate of length along line after being provided with percent and result of newlineinfo'''
	total=0
	for n in line:
		total+=n[2]
	if dist>total:
		return -1
	tot2=0
	for n in line:
		tot2+=n[2]
		if tot2>=dist:
			along=dist-(tot2-n[2])
			sign=math.copysign(1,n[1][0]-n[0][0])
			x=n[0][0]+(along*n[3][0])
			y=n[0][1]+(along*n[3][1])
			break
	return x,y
	
	
def polyline(plist,dist):
	'''return a list of dots, split by dist
	'''
	respoints=[]
	respoints.append(plist[0][0])
	lineleft=0
	for lines in plist:
		linedat=asline(lines)
		linelen=linedat[2]
		lineleft+=linedat[2]
		while lineleft>=dist:
			pc=(linelen-lineleft)/linelen
			respoints.append(pcline(pc,linedat))
			lineleft-=dist
	print respoints
	
def plinesplit(plist,dist):
	'''return a list of dots, split by dist
	'''
	retlist=[]
	ret=0
	ct=0
	while ret<>-1:	
		ret=distline(ct,asline(plist))
		retlist.append(ret)
		ct+=dist
	return retlist[:-1]

	
def routecalc(filename='route.py',dist=10):
	'''take a list of points from a file and returns a list of points split by every dist meters
	filename = list of co-ordinates split by space
	dist fistsnce to split lines into
	return
	list of points [[x,y],[x1,y1]
	'''
	points=[]
	with open(filename,'r') as file:
		for line in file.readlines():
			points.append([float(line.rstrip().split(' ')[0]),float(line.rstrip().split(' ')[1])])
	
	mx,my=min(points,key=lambda x:x[0])[0],min(points,key=lambda x:x[1])[1]
	
	result=plinesplit(points,dist)
	return result
	
def simpleline(filename='route.py'):
	points=[]
	with open(filename,'r') as file:
		for line in file.readlines():
			points.append([float(line.rstrip().split(' ')[0]),float(line.rstrip().split(' ')[1])])
	return points
	
'''

points=[[(n[0]-mx),(n[1]-my)] for n in points]

import canvas
w = h = 100
canvas.set_size(w, h)
for x,y in plinesplit(points,10):
	canvas.fill_pixel(x,y)

			'''
			
