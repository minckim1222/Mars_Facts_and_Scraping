#import libraries
from flask import Flask, render_template, redirect
import pymongo
import Mission_to_Mars
#create flask app
app = Flask(__name__)

#create pymongo client
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars

@app.route("/")
def home():
    data = list(db.collection.find())
    print(data)
    return render_template("index.html", data = data)

@app.route("/scrape")
def scrape_data():
    data = Mission_to_Mars.scrape()
    db.collection.remove({})
    db.collection.insert_one(data)
    return redirect('http://127.0.0.1:5000/')


if __name__ == "__main__":
    app.run(debug=True)