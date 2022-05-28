from flask import Flask, render_template
from pymongo import MongoClient

from config import data


app = Flask(__name__)
client = MongoClient(data["connent"])
users = client.website.users


@app.route("/")
def index():
	message = users.find_one({})["messages"]
	return render_template("index.html",
		messages=messages[::-1]
		)

if __name__ == "__main__":
	app.run(**data["run"])
