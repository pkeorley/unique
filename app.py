from flask import Flask
from pymongo import MongoClient

from config import data


app = Flask(__name__)
client = MongoClient(data["connent"])
users = client.website.users


@app.route("/")
def index():
	return "Прівєтік жабка."

if __name__ == "__main__":
	app.run(**data["run"])
