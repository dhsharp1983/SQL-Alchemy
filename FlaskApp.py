# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column
from datetime import datetime
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# Map DB into Classes automatically 
Base = automap_base()

# reflect the database from the engine 
Base.prepare(engine, reflect=True)

# Establish connection with the database 
# session = Session()
session = Session(bind = engine)

# Map DB Base Classes to Variables for Querying 
Measurement = Base.classes.measurement
Station = Base.classes.station

# Get start_date value
min_date = session.query(func.min(Measurement.date)).scalar()
max_date = session.query(func.max(Measurement.date)).scalar()
start_date = dt.datetime.strptime(max_date, '%Y-%m-%d') - dt.timedelta(days = 365)
session.close()

# Create Flask App
app = Flask(__name__)

# Create Flask Routes
@app.route("/")
def homepage():
    return(
    f"Welcome! <br>"
    f"Available Routes:<br>"
    f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br>"
    f"<a href='/api/v1.0/precip'>/api/v1.0/precip</a>")

@app.route("/api/v1.0/stations")
def stations():
    StationList = session.query(Station.id, Station.station, Station.name).all()
    session.close()
    return jsonify (StationList=StationList)

@app.route("/api/v1.0/precip")
def precip():
    PrecipQuery = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).order_by(Measurement.date).all()
    session.close()
    PrecipDictionary = {}
    for entry in PrecipQuery:
        PrecipDictionary[entry[0]] = entry[1]

    return jsonify (PrecipDictionary = PrecipDictionary)

if __name__ == '__main__':
    app.run(debug = True)

