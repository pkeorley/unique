from flask import Flask, render_template
from pymongo import MongoClient

from config import data


app = Flask(__name__)
client = MongoClient(data["connent"])
users = client.website.users


@app.route("/")
def index():
	history = users.find_one({})["messages"]
	all_messages = [[m[0], m[1].replace("<", "").replace(">", "").replace("&", "")] for m in history]
	all_messages = [m[1] for m in all_messages]
	all_words = " ".join(all_messages).split()
	all_symbols = len("".join(all_words))
	return render_template("index.html",
	    messages=history,
            all_messages=len(all_messages),
	    all_words=len(all_words),
	    all_symbols=all_symbols
	)


if __name__ == "__main__":
	app.run(**data["run"])
