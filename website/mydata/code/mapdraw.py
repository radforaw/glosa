import folium
import geometryfunctions as g

def mapdraw(locations):
	tx=[x[0] for x in locations]
	ty=[x[1] for x in locations]
	centre=g.OSGB36toWGS84(sum(tx)/len(tx),sum(ty)/len(ty))
	m=folium.Map(location=centre,zoom_start=13,width=640,height=480)
	for y in range(len(locations)-1):
		locs=[g.OSGB36toWGS84(locations[y][0],locations[y][1]),g.OSGB36toWGS84(locations[y+1][0],locations[y+1][1])]
		folium.PolyLine(locs,color="black",weight=8).add_to(m)
	for y in range(len(locations)-1):
		locs=[g.OSGB36toWGS84(locations[y][0],locations[y][1]),g.OSGB36toWGS84(locations[y+1][0],locations[y+1][1])]
		folium.PolyLine(locs,color=col(locations[y][2]),weight=6).add_to(m)
	html=m.get_root().render()
	return html


	
def col(c):
	ret="black"
	if c=="Red":
		ret='red'
	if c=="Amber":
		ret='yellow'
	if c=="Green":
		ret='green'		
	if c=="RedAmber":
		ret='orange'
	return ret
