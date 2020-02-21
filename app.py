from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt


####################################################################
# Database Setup
####################################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect database into a model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

####################################################################
# Flask Setup
####################################################################

app = Flask(__name__)

####################################################################
# Flask Routes
####################################################################

@app.route("/")
def home():
    return(
        f"Welcome to my home page!<br/>"
        f"For more content go to:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session from Python to the DB
    session = Session(engine)
    
    # Query
    lastestmeasurement = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()
    
    twelveMonthsAgo = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    lastyearofdata = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > twelveMonthsAgo).\
    order_by(Measurement.date.desc()).all()
    
    session.close()
    
    # Create a list of dictionaries from the data queried above
    all_precipitation = []
    for date, prcp in lastyearofdata:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        all_precipitation.append(precipitation_dict)
        
    return jsonify(all_precipitation)
  
@app.route("/api/v1.0/stations")
def stations():
    # Create session from Python to the DB
    session = Session(engine)
    
    # Query
    stations = session.query(Measurement.station).\
    group_by(Measurement.station).all()
    
    session.close()
    
    # Create a list of the query data
    all_stations = []
    for station in stations:
        all_stations.append(station)
        
    return jsonify(all_stations)
    
    
@app.route("/api/v1.0/tobs")
def temperature():
    # Create session from Python to the DB
    session = Session(engine)
    
    # Query
    temps = session.query(Measurement.station, func.count(Measurement.tobs)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.tobs).desc()).all()
    
    session.close()
    
    # Create a list of dictionaries from the query data
    all_temps = []
    for station, tobs in temps:
        temp_dict = {}
        temp_dict['station'] = station
        temp_dict['tobs'] = tobs
        all_temps.append(temp_dict)
        
    return jsonify(all_temps)
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    