#Import Dependencies
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine 
from sqlalchemy import func

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
most_active_station='USC00519281'


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
    session = Session(engine)
    #Query to get the temperatures associated to the most active station
    most_active_12=session.query(Measurement.date,Measurement.tobs). \
                    filter(Measurement.date.between(start_day , end_day), \
                           Measurement.station ==most_active_station). \
                           order_by(Measurement.date).all()

    #Close the session
    session.close()
    #Create a dictionary to jsonify
    tobs=dict((x, y) for x, y in most_active_12)

    return jsonify(tobs) 

@app.route("/api/v1.0/<start>")
def temp_w_start(start):
    """Returns max, min and average temperature from the start day specified. \
                    If the start date doesn't exist the path returns the error 404"""
    #Find the correct format and convert string to database format
    try:
        is_year_first=int(start[0:4])
        first_date = str(start) 
    except:
       return jsonify({"Format error ": f"Please write the date in a  yyyy-mm-dd format"}), 404    
    else:
    #Check for the date in the table
        if is_year_first>=2010 and is_year_first<=2017:
            #Open the session
            session = Session(engine)
            #Query the tempertures in the period of time
            temperatures=session.query(Measurement.station,func.min(Measurement.tobs), \
                func.max(Measurement.tobs),func.avg(Measurement.tobs)). filter(Measurement.date >= first_date, \
                Measurement.station == most_active_station).all()
            #Close session
            session.close
            #Create a dictionary
            temps_dict={} 
            temps_dict={f"{temperatures[0][0]}": [f"{temperatures[0][1]} (min)",f"{temperatures[0][2]} (max)",\
                    f"{temperatures[0][3]:0.2f} (average)"]} 
            return jsonify(temps_dict)
        else:
            return jsonify({"error": f"The date {first_date} is incorrect.Enter date between 2010-01-01 and 2017-08-23"}), 404

@app.route("/api/v1.0/<string:start>/<string:end>")
def temp_w_end(start,end):
    """Returns max, min and average temperature between two dates as json. \
                    If any of them don't exist the path returns error 404"""
    #Confirm the dates are in the database
    try:
        is_s_year_first=int(start[0:4]) 
    except:
        return jsonify({"Format error ": f"Please write the start date in a  yyyy-mm-dd format"}), 404    
    else:
        try:
            is_e_year_first=int(end[0:4])
        except:
            return jsonify({"Format error ": f"Please write the end date in a  yyyy-mm-dd format"}), 404  
        else:
        #Check for the date in the table
            if (is_s_year_first>=2010 and is_s_year_first<=2017) and (is_e_year_first>=2010 and is_e_year_first<=2017):
                #Open the session
                session = Session(engine)
                #Query the tempertures in the period of time
                temp_start_end=session.query(Measurement.station,func.min(Measurement.tobs), \
                        func.max(Measurement.tobs),func.avg(Measurement.tobs)). \
                        filter(Measurement.date.between(start,end), \
                        Measurement.station == most_active_station).all()
                #Close session
                session.close
                #Create a dictionary
                new_temps_dict={} 
                new_temps_dict={f"{temp_start_end[0][0]}": [f"{temp_start_end[0][1]} (min)",f"{temp_start_end[0][2]} (max)",\
                    f"{temp_start_end[0][3]:0.2f} (average)"]} 
                return jsonify(new_temps_dict)
            else:
                return jsonify({"error": f"{start} or {end} dates are incorrect.Try enter dates between 2010-01-01 and 2017-08-23"}), 404 
                #Close session
                session.close

@app.route("/")
def welcome():
    return (
        f"<p><h2>Welcome to Hawaii's weather API!<h2><p/>"
        f"<h4>Available Routes:<h4><br/>"
        f"/api/v1.0/precipitation<br/>"   
        f"/api/v1.0/station<br/>"  
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2014-08-23 <br/> "
        f"/api/v1.0/2016-08-23/2017-08-23 <br/>"
    )

#Debug errors everytime the code runs
if __name__ == "__main__":
    app.run(debug=True)