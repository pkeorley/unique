from flask import Flask, render_template
from pymongo import MongoClient

from config import data


app = Flask(__name__)
client = MongoClient(data["connent"])
users = client.website.users


@app.route("/")
def index():
	message = users.find_one({})
	return render_template("index.html",
		last_message_content=message["last_message_content"].replace("&", "").replace("<", "").replace(">", ""),
		last_message_id=message["last_message_id"],
		last_message_created_at=message["last_message_created_at"]
		)

if __name__ == "__main__":
	app.run(**data["run"])
