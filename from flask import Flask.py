from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import numpy as np
import pandas as pd

from flask import Flask, jsonify

import datetime as dt
from datetime import timedelta

# create engine
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)

# reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


# step 1:
app = Flask(__name__)

@app.route("/")
def welcome():
    session = Session(engine)
    # urls that tell the user the end points that are available
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Last Year of Percipitation Data"""
    session = Session(engine)
    #find last date in database from Measurements 
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    #convert last date string to date

    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")

    #calculate date one year after last date using timedelta datetime function
    first_date = last_date - timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).all()
    return jsonify(last_year_data)

@app.route("/api/v1.0/stations")
def stations():
    # return a list of all the stations in JSON Format
    listOfStations = session.query(Station.station).all()
    
    stationOneDimension = list(np.ravel(listOfStations))
    return jsonify(stationOneDimension)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #find last date in database from Measurements 
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    #convert last date string to date

    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")

    #calculate date one year after last date using timedelta datetime function
    first_date = last_date - timedelta(days=365)
    
    station_counts = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    top_station = (station_counts[0])
    top_station = (top_station[0])
    
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == top_station).all()
    
    top_station_year_obs = session.query(Measurement.tobs).\
    filter(Measurement.station == top_station).filter(Measurement.date >= first_date).all()



#2nd step:
if __name__ == '__main__':
    app.run()