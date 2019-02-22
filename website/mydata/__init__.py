from flask import Flask
from flask import make_response, request, render_template
#from flask_cors import CORS
import time
import os
import csv
import datetime

import code

app = Flask(__name__,static_url_path="/static")

#cors=CORS(app,resources={r"*":{"origins":"*"}})

@app.route("/")
def hello():
	db1=code.mysql()
	return render_template('list.html',posts=db1.getdrivers(),titles=["Drivers","Runs"],href="drivers",intro="This is a list of all the drivers, by number of runs",arg=[])


@app.route("/drivers")
def drivers():
	args=request.args.to_dict()
	db2=code.mysql()
	return render_template('list.html',posts=db2.getdriverroutes(args['data']),titles=["Route","Runs"],href="runs",intro="This is a list of all the drivers, by number of runs",arg=[args['data']])

@app.route("/runs")
def runs():
	args=request.args.to_dict()
	db3=code.mysql()
	posts=db3.getdriverroutesjourney(args['data2'],args['data'])
	posts=[[x[0],time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(x[1]))] for x in posts]
	return render_template('list.html',posts=posts,titles=["Run","Date"],href="summary",intro="This is a list of all runs by "+args['data2']+' on the '+args['data']+' leg.',arg=[])

@app.route("/maps")
def maps():
	args=request.args.to_dict()
	db4=code.mysql()
	return code.mapdraw(db4.getmapdata(args['data']))

@app.route("/graph")
def graph():
	args=request.args.to_dict()
	db5=code.mysql()
	response = make_response(code.graphdraw(db5.getmapdata(args['data']),args['data']).read())
	response.headers.set('Content-Type', 'image/png')
	response.headers.set('Content-Disposition', 'inline')
	return response

@app.route("/summary")
def summary():
	db=code.mysql()
	args=request.args.to_dict()
	return render_template('summary.html',data=args['data'])
