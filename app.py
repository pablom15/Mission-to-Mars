from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["DATABASE_URL"] = "postgres://ttsskopxdmnsfo:4378043c6d59d120e32dd53458a7b496edba8ae3199207429f3709d03c59db82@ec2-52-203-165-126.compute-1.amazonaws.com:5432/d4arif9evev4vq"
mongo = SQLAlchemy(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

@app.route("/Cerberus Hemisphere Enhanced")
def show_hemi_1():
   image = scraping.image_hemisphere(0)
   return render_template("hemi1.html", image=image)

@app.route("/Schiaparelli Hemisphere Enhanced")
def show_hemi_2():
   image = scraping.image_hemisphere(1)
   return render_template("hemi2.html", image=image)

@app.route("/Syrtis Major Hemisphere Enhanced")
def show_hemi_3():
   image = scraping.image_hemisphere(2)
   return render_template("hemi3.html", image=image)

@app.route("/Valles Marineris Hemisphere Enhanced")
def show_hemi_4():
   image = scraping.image_hemisphere(3)
   return render_template("hemi4.html", image=image)

if __name__ == "__main__":
   app.run()