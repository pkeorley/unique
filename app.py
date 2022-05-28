from flask import Flask
from pymongo import MongoClient

from config import data


app = Flask(__name__)
client = MongoClient(data["connent"])
users = client.website.users


@app.route("/")
def index():
	message = users.find_one({})
	return """<h1>Information of Quanted</h1>
	<p><b>Last message content:</b> {}</p>
	<p><b>Last message id:</b> {}</p>
	<p><b>Last message created at:</b> {}</p>""".format(
		message["last_message_content"].replace("<", "[").replace(">", "]")),
		message["last_message_id"],
		message["last_message_created_at"]
	)

if __name__ == "__main__":
	app.run(**data["run"])
