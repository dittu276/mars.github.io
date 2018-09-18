# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_info

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars_facts = scrape_info.scrape_mars()

    # Store results into a dictionary
    mars = {
        "News Title": mars_facts["news_title"],
        "News Paragraph": mars_facts["news_p"],
        "Featured Image": mars_facts["featured_image_url"],
        "Mars Weather": mars_facts["mars_weather"],
        "Mars Facts":mars_facts["fact_table"],
        "Hemisphere Images": mars_facts["hemisphere_image_urls"]
    }

    # Insert forecast into database
    mongo.db.collection.insert_one(mars)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
