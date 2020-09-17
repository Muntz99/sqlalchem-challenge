from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
# create engine
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
# step 1:
app = Flask(__name__)
@app.route("/")
def helloWorld():
    # urls that tell the user the end points that are available
    return "Hello World"
#2nd step:
if __name__ == '__main__':
    app.run()