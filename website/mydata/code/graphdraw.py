import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io

def graphdraw(locations,journey):
	locations = sorted(locations, key=lambda x:x[3])
	starttime=locations[0][3]
	plt.scatter([x[3]-starttime for x in locations],[x[4] for x in locations],color=[newcol(x[2]) for x in locations])
	plt.plot([x[3]-starttime for x in locations],[x[4] for x in locations],color='grey')

	plt.title('Journey '+journey)
	buf=io.BytesIO()
	plt.savefig(buf, format='png',dpi=90)
	buf.seek(0)
	plt.close()
	return buf


def newcol(c):
	ret="k"
	if c=="Red":
		ret='r'
	if c=="Amber":
		ret='y'
	if c=="Green":
		ret='g'		
	if c=="RedAmber":
		ret='c'
	return ret
