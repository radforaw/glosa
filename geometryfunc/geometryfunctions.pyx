from math import sqrt, pi, sin, cos, tan, atan2


def WGS84toOSGB36(double lat, double lon):
	""" Accept latitude and longitude as used in GPS.
	Return OSGB grid coordinates: eastings and northings.
	Usage:
	>>> from latlon_to_bng import WGS84toOSGB36
	>>> WGS84toOSGB36(51.4778, -0.0014)
	(538890.1053365842, 177320.49650700082)
	>>> WGS84toOSGB36(53.50713, -2.71766)
	(352500.19520169357, 401400.01483428996)
	"""
	# First convert to radians
	# These are on the wrong ellipsoid currently: GRS80. (Denoted by _1)
	cdef double lat_1 = lat*pi/180
	cdef double lon_1 = lon*pi/180
	
	# Want to convert to the Airy 1830 ellipsoid, which has the following:
	# The GSR80 semi-major and semi-minor axes used for WGS84(m)
	cdef double a_1,b_1,e2_1,nu_1,H,x_1,y_1,z_1,s

	a_1, b_1 = 6378137.000, 6356752.3141
	e2_1 = 1 - (b_1*b_1)/(a_1*a_1)  # The eccentricity of the GRS80 ellipsoid
	nu_1 = a_1/sqrt(1-e2_1*sin(lat_1)**2)
	
	# First convert to cartesian from spherical polar coordinates
	H = 0  # Third spherical coord.
	x_1 = (nu_1 + H)*cos(lat_1)*cos(lon_1)
	y_1 = (nu_1 + H)*cos(lat_1)*sin(lon_1)
	z_1 = ((1-e2_1)*nu_1 + H)*sin(lat_1)
	
	# Perform Helmut transform (to go between GRS80 (_1) and Airy 1830 (_2))
	s = 20.4894*10**-6  # The scale factor -1
	# The translations along x,y,z axes respectively
	cdef double tx, ty, tz 
	tx,ty,tz= -446.448, 125.157, -542.060
	# The rotations along x,y,z respectively, in seconds
	cdef double rxs, rys, rzs
	rxs,rys,rzs = -0.1502, -0.2470, -0.8421
	# In radians
	cdef double rx, ry, rz
	rx,ry,rz = rxs*pi/(180*3600.), rys*pi/(180*3600.), rzs*pi/(180*3600.)
	cdef double x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1
	cdef double y_2 = ty + (rz)*x_1 + (1+s)*y_1 + (-rx)*z_1
	cdef double z_2 = tz + (-ry)*x_1 + (rx)*y_1 + (1+s)*z_1
	
	# Back to spherical polar coordinates from cartesian
	# Need some of the characteristics of the new ellipsoid
	# The GSR80 semi-major and semi-minor axes used for WGS84(m)
	cdef double a, b 
	a,b= 6377563.396, 6356256.909
	cdef double e2 = 1 - (b*b)/(a*a)  # The eccentricity of the Airy 1830 ellipsoid
	cdef double p = sqrt(x_2**2 + y_2**2)
	
	# Lat is obtained by an iterative proceedure:
	lat = atan2(z_2, (p*(1-e2)))  # Initial value
	cdef double latold = 2*pi
	while abs(lat - latold) > 10**-16:
		lat, latold = latold, lat
		nu = a/sqrt(1-e2*sin(latold)**2)
		lat = atan2(z_2+e2*nu*sin(latold), p)
		
	# Lon and height are then pretty easy
	lon = atan2(y_2, x_2)
	H = p/cos(lat) - nu
	
	# E, N are the British national grid coordinates - eastings and northings
	cdef double F0 = 0.9996012717  # scale factor on the central meridian
	cdef double lat0 = 49*pi/180  # Latitude of true origin (radians)
	cdef double lon0 = -2*pi/180  # Longtitude of true origin and central meridian (radians)
	cdef double N0, E0 
	N0,E0= -100000, 400000  # Northing & easting of true origin (m)
	cdef double n = (a-b)/(a+b)
	
	# meridional radius of curvature
	cdef double rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
	cdef double eta2 = nu*F0/rho-1
	
	cdef double M1 = (1 + n + (5/4)*n**2 + (5/4)*n**3) * (lat-lat0)
	cdef double M2 = (3*n + 3*n**2 + (21/8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
	cdef double M3 = ((15/8)*n**2 + (15/8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
	cdef double M4 = (35/24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
	
	# meridional arc
	cdef double M = b * F0 * (M1 - M2 + M3 - M4)
	
	cdef double I = M + N0
	cdef double II = nu*F0*sin(lat)*cos(lat)/2
	cdef double III = nu*F0*sin(lat)*cos(lat)**3*(5 - tan(lat)**2 + 9*eta2)/24
	cdef double IIIA = nu*F0*sin(lat)*cos(lat)**5*(61 - 58*tan(lat)**2 + tan(lat)**4)/720
	cdef double IV = nu*F0*cos(lat)
	cdef double V = nu*F0*cos(lat)**3*(nu/rho - tan(lat)**2)/6
	cdef double VI = nu*F0*cos(lat)**5*(5 - 18*tan(lat)**2 + tan(lat)**4 + 14*eta2 - 58*eta2*tan(lat)**2)/120
	
	N = I + II*(lon-lon0)**2 + III*(lon-lon0)**4 + IIIA*(lon-lon0)**6
	E = E0 + IV*(lon-lon0) + V*(lon-lon0)**3 + VI*(lon-lon0)**5
	
	# Job's a good'n.
	return E, N



def dist( a, b):
	cdef double x,y
	x=a[0]-b[0]
	y=a[1]-b[1]
	return sqrt(x*x+y*y)

def angle( a, b):
	cdef double x,y,r
	x=b[0]-a[0]
	y=b[1]-a[1]
	r=atan2(x,y)*(180/pi)
	#if r<0:
	#	r+=180
	return r%360

def closething(point,double ang,data):
	'''determine if a point is near to and going in the same direction as a line
	point = location (easting, northing)
	ang = 0-360 heading
	data = list of points showing the line that is being compared.
	'''
	#res=min([[((point[0]-data[n][0])**2)+((point[1]-data[n][1])**2),n] for n in xrange(len(data)-1)])
	
	res=min([[pointlinedistance((data[0],data[1]), point)[1],n] for n in xrange(len(data)-1)])
	if res[0]<100 and res[1]<len(data): #close but not last point
		aa=angle(data[res[1]],data[res[1]+1])
		if 180-abs(abs(ang-aa)-180)<45: # within 90 degrees of expected
			return True
	return False

def pointlinedistance(line,point):
	cdef double x1,y1,x2,y2,x3,y3,u,ix,iy,d
	x1=line[0][0]
	y1=line[0][1]
	x2=line[1][0]
	y2=line[1][1]
	x3=point[0]
	y3=point[1]
	u=(((x3-x1)*(x2-x1))+((y3-y1)*(y2-y1)))/(((x2-x1)**2)+((y2-y1)**2))
	if u<0.0001 or u>1:
		if ((x3-x1)**2)+((y3-y1)**2)<((x3-x2)**2)+((y3-y2)**2):
			ix=x1
			iy=y1
		else:
			ix=x2
			iy=y2
	else:
		ix = x1 + u * (x2 - x1)
		iy = y1 + u * (y2 - y1)
	d=((ix-x3)**2)+((iy-y3)**2)
	return (ix,iy),d
