import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///hawaii.sqlite")

conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in query}
    return jsonify(precip)

@app.route("/api/v1.0/tobs")
def names():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query1 = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station=="USC00519281").filter(Measurement.date >= prev_year).all() 
    return jsonify(query1)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    temp_station=session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start).all()
    return jsonify(temp_station)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    session = Session(engine)
    temp_stationQ=session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    return jsonify(temp_stationQ)

@app.route("/api/v1.0/<stations>")
def stations():
    session = Session(engine)
    station = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    return jsonify(station)



if __name__ == '__main__':
    app.run(debug=True)