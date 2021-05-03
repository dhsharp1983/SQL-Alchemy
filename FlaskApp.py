# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column
from datetime import datetime
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# Map DB into Classes automatically 
Base = automap_base()

# reflect the database from the engine 
Base.prepare(engine, reflect=True)

# Establish connection with the database 
session = Session(bind = engine)

# Map DB Base Classes to Variables for Querying 
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Flask App
app = Flask(__name__)

# Create Flask Routes
@app.route("/")
def homepage():
    return(
    f"Welcome! <br>"
    f"Available Routes:<br>"
    f"/api/v1.0/stations")

@app.route("/api/v1.0/stations")
def stations():
    Var = session.query(Station.id, Station.station, Station.name).all()
    session.close()
    return jsonify (Var=Var)

if __name__ == '__main__':
    app.run(debug = True)
