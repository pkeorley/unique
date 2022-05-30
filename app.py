from flask import Flask, render_template, request, redirect, , jsonify
from pymongo import MongoClient

from config import data


app = Flask(__name__)
client = MongoClient(data["connent"])
users = client.website.users
invites = client.website.invites

@app.route("/", methods=["GET", "POST"])
def login():
    if request.cookies.get("logined"):
        return redirect("/chat")
    if request.method == "POST":
        password = request.form.get("password")
        if password == "putinpidaras":
            cookies = make_response(redirect("/chat"))
            cookies.set_cookie("logined", "true")
            return cookies
        else:
            return "Не верный пароль! Перезагрузите страницу..."
    return """<form method="post"><p><b>Введите пароль для входа на сайт:</b> <input name="password" id="password"></p><button>Try login</button></form>"""

@app.route("/chat")
def chat():
    if not request.cookies.get("logined"): return redirect("/")
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


@app.route("/invite/<key>")
def invite_(key):
    invite = invites.find_one({
        "type": "invite",
        "key": key
    })
    if invite is not None:
        return redirect(invite["url"])
    return "<p class=\"error\">Unknown key</p>"


@app.route("/api/invite/create/", methods=["GET", "POST"])
def api_create_invite():
    if request.method == "GET":
        args = ("key" in request.args, "url" in request.args, "api_key" in request.args)
        if all(args) is False:
            return jsonify({
                "error": {
                    "text": "Отсутствует один из аргументов (key, url, api_key)",
                    "args": {
                        "key": args[0],
                        "url": args[1],
                        "api_key": args[1]
                    }
                },
                "example": "http://www.pkeorley.ml/api/invite/create/?key=google&url=https://google.com/&api_key=pLQNGMyCclqOOEUD"
            })
        elif all(args) is True:
            if not invites.count_documents() == 0:
                return jsonify({
                    "error": {
                        "text": "Данный ключ уже есть в базе данных"
                    }
                })
            else:
                invites.update_one(invite, {"$inc": {
                    "used": 1,
                    "uses": -1
                }})
                


if __name__ == "__main__":
    app.run(**data["run"])
