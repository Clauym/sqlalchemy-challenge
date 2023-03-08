#Import Dependencies
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import sqlite3

#Import Flask module
from flask import Flask, jsonify

# Set up the connection to the database
engine = create_engine("sqlite:///./Resources/hawaii.sqlite",echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the tables
Measurement=Base.classes.measurement 
Station = Base.classes.station

# Create an app on Flask
app = Flask(__name__)

start_day='2016-08-23'
end_day='2017-08-23'

@app.route("/api/v1.0/precipitation")
def max_precipitation():
    """Return the maximum precipitation per day in Hawaii database as json"""

    #Open and close the session in each tab to avoid leaving a session open
    session = Session(engine)
    # Query max precipitation for every observation in the database
    precip_12_months=session.query(Measurement.date,func.max(Measurement.prcp)). \
                    filter(Measurement.date.between(start_day , end_day)). \
                    group_by(Measurement.date).order_by(Measurement.date.asc()).all() 
    #Close the session
    session.close()
    #Create a dictionary to jsonify
    precip_12_dict = dict((x, y) for x, y in precip_12_months)

    return jsonify(precip_12_dict)

@app.route("/api/v1.0/station")
def stations_number():
    """Return the number of weather stations in Hawaii database as json"""
    #Open and close the session in each tab to avoid leaving a session open
    session = Session(engine)
    #Query the number of stations in the database
    stations=session.query(Station.station,Station.name).order_by(Station.name.asc()).all()
    #Close the session
    session.close()
    #Create a dictionary to jsonify
    station_list = dict((x, y) for x, y in stations)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_obs():
    """Return the temperature observations for the last year in the database as json"""
    
    #Open the session in each tab to avoid leaving a session open
    most_active_station='USC00519281'
    
    
    session = Session(engine)
    #Query to get the temperatures associated to the most active station
    most_active_12=session.query(Measurement.date,Measurement.tobs). \
                    filter(Measurement.date.between(start_day , end_day), \
                           Measurement.station ==most_active_station). \
                           order_by(Measurement.date).all()

    #Close the session
    session.close()
    
    tobs=dict((x, y) for x, y in most_active_12)

    return jsonify(tobs) 

#@app.route("/api/v1.0/<start>")
#def temp_w_start(start_date):
#    """Returns max, min and average temperature from the start day specified as json. \
#                    If it doesn't exist the path returns the error 404"""
    #session = Session(engine)
    # Query all temps
    #results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
    #session.close()

#    return jsonify({"error": f"The date {start_date} was not found."}), 404

#@app.route("/api/v1.0/<start>/<end>")
#def temp_w_start_end(start_date,end_date):
#    """Returns max, min and average temperature between two dates as json. \
#                    If any of them don't exist the path returns error 404"""
    
    #session = Session(engine)
    # Query all temps
    #results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
    #session.close()
#   return jsonify({"error": f"Either of the dates {start_date} or {end_date} were not found."}), 404

#Defining what to do in the index
@app.route("/")
def welcome():
    return (
        f"<p>Welcome to Hawaii's weather API!<p/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"   
        f"/api/v1.0/station<br/>"  
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Debug ewrrors everytime we run the code
if __name__ == "__main__":
    app.run(debug=True)