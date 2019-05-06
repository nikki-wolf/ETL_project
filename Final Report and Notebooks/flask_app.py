from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/world_development_indicator_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    world_dev_data = mongo.db.wdi_general.find_one()

    # Return template and data
    return render_template("index.html", indicators=world_dev_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    



if __name__ == "__main__":
    app.run(debug=True)
