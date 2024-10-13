# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home_page():
    """Return a home page with various route options according to challenge instructions"""
    return (
        f"You are now at Morgan Bee's Module 10 Challenge Home Page.<br/>"
        f"Available Routes<br/>"
        f"---------------------------------------------------------------<br/>"
        f"Static Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations<a/><br/>"
        f"<a href='/api/v1.0/tobs'>TOBS<a/><br/>"
        f"---------------------------------------------------------------<br/>"
        f"Dynamic Routes:<br/>"
        f"Find temperature summary from a start date (MMDDYYYY):<br/>"
        f"/api/v1.0/start_date<br/>"
        f"Find temperature summary between two dates (MMDDYYYY):<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a jsonified dictionary of dates and precipitation data from the
    last year in the database"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find last 12 months of precipitation data
    # Start with most recent date
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()
    most_recent_date = pd.to_datetime(most_recent[0]).date()
    
    # Find one year ago
    year_ago =  most_recent_date - dt.timedelta(days=365)
    
    # Query for precipitation data over the past year
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date <= most_recent_date).\
        filter(measurement.date >= year_ago).\
        order_by(measurement.date)
    
    # Close session
    session.close()

    # Create empty dictionary
    prcp_data_dict = {}

    # Add values to dictionary
    for date, prcp in precipitation:
        prcp_data_dict[date] = prcp

    # Return dictionary of dates and precipitation data
    return jsonify(prcp_data_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a jsonified list of the stations in the database"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find all stations from the dataset
    stations = session.query(func.distinct(measurement.station)).all()

    # Close session
    session.close()

    # Create empty list for data
    station_list = []

    # Print station names into list
    for station in stations:
        station_list.append(station[0])

    # Return list of stations
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temperatures():
    """Return a jsonified list of the temperature data collected at the most 
    active station from the last year in the database"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most active station in the dataset
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    printed_stations = [station for station, count in active_stations]
    most_active_station = printed_stations[0]

    # Find most recent date
    most_recent = session.query(measurement.date).order_by(measurement.date.desc()).first()
    most_recent_date = pd.to_datetime(most_recent[0]).date()

    # Calculate one year ago
    year_ago =  most_recent_date - dt.timedelta(days=365)

    # Query dates and temperature observations for most active station over the past year
    most_active_temps = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == most_active_station).\
    filter(measurement.date <= most_recent_date).\
    filter(measurement.date >= year_ago).all()

    # Close session
    session.close()

    # Create empty list for data
    active_temps_list = []

    # Print dates and temps into list
    for date, temp in most_active_temps:
        active_temps_list.append(temp)

    # Return most active station's temperature recordings from the past year
    return jsonify(active_temps_list)

@app.route("/api/v1.0/<start>")  
def temps_from_start_date(start):
    """Return a jsonified dictionary of the minimum, maximum, and average temperature
    from a specified start date onward"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Format date input
    start_formatted = pd.to_datetime(start, format = "%m%d%Y").date()

    # Take min, max, avg of tobs
    sel = [func.min(measurement.tobs), 
           func.max(measurement.tobs),
           func.avg(measurement.tobs)]
    
    # Query for temps from the start date onward
    start_temp_calculations = session.query(*sel).\
        filter(measurement.date >= start_formatted).all()

    # Close session
    session.close()

    # Create empty dictionary for temperature information
    start_temp_info_dict = {}

    # Add temp info from query into dictionary, in format that is accepted
    for temps in start_temp_calculations:
        start_temp_info_dict["Temps"] = list(start_temp_calculations[0])

    #return f"The minimum, maximum, and average temperature from {start} onwards are:"
    return jsonify(start_temp_info_dict)


@app.route("/api/v1.0/<start>/<end>")  
def temps_between_dates(start, end):
    """Return a jsonified dictionary of the minimum, maximum, and average temperature
    between a specified start date and specified end date"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Format date input
    start_formatted = pd.to_datetime(start, format = "%m%d%Y").date()
    end_formatted= pd.to_datetime(end, format = "%m%d%Y").date()

    # Take min, max, avg of tobs
    sel = [func.min(measurement.tobs), 
           func.max(measurement.tobs),
           func.avg(measurement.tobs)]
    
    # Query for temps from the start date to end date, inclusive
    start_end_temp_calculations = session.query(*sel).\
        filter(measurement.date >= start_formatted).\
        filter(measurement.date <= end_formatted).all()
    
    # Close session
    session.close()

    # Create empty dictionary for temperature information
    start_end_temp_info_dict = {}

    # Add temp info from query into dictionary, in format that is accepted
    for temps in start_end_temp_calculations:
        start_end_temp_info_dict["Temps"] = list(start_end_temp_calculations[0])

    #return f"The minimum, maximum, and average temperature from {start} onwards are:"
    return jsonify(start_end_temp_info_dict)

if __name__ == '__main__':
    app.run(debug=True)