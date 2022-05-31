import random
import string

from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient

from config import data


app = Flask(__name__)
client = MongoClient(data["connent"])
users = client.website.users
invites = client.website.invites
economc = clent.website.economic


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
    return jsonify({
        "error": {
            "text": "Неизвестный ключ"
        }
    })


@app.route("/api/v1/shortlink/create", methods=["GET", "POST"])
def api_invite_create():
    if request.method == "GET":
        args = [
            "key" in request.args,
            "url" in request.args,
            "api_key" in request.args
        ]
        if all(args) is False:
            return jsonify({
                "error": {
                    "text": "Missing one of the arguments in the link",
                    "solution": "Enter all three arguments"
                },
                "example": "http://www.pkeorley.ml/api/v1/shortlink/create?api_key=pLQNGMyCclqOOEUD&key=google&url=https://google.com/"
            })
        elif all(args) is True:
            if invites.count_documents({
                "type": "api_key",
                "key": request.args["api_key"]
            }) == 0:
                return jsonify({
                 "error": {
                     "text": "Invalid api key",
                     "solution": "Ask peaky to issue/replace you with a new api key"
                    }
                })
            elif invites.count_documents({
                "type": "invite",
                "key": request.args["key"]
            }) != 0:
                return jsonify({
                    "error": {
                        "text": "This key already exists",
                        "solution": "Try entering a different key name"
                    }
                })
            elif invites.find_one({
                "type": "api_key",
                "key": request.args["api_key"]
            })["uses"] <= 0:
                return jsonify({
                    "error": {
                        "text": "Not enough usage keys",
                        "solution": "Ask peaky to give you usage points"
                    }
                })
   
            invites.update_one({
                "type": "api_key",
                "key": request.args["api_key"]
            }, {"$inc": {
                "used": 1,
                "uses": -1
            }, "$push": {
                "shortlinks": request.args["key"]
            }})
            invites.insert_one({
                "type": "invite",
                "key": request.args["key"],
                "url": request.args["url"]
            })
            return jsonify({
                "result": f"http://www.pkeorley.ml/invite/{request.args['key']}"
            })

    elif request.method == "POST":
        request_json = request.json or {}
        args = [
            "key" in request_json,
            "url" in request_json,
        ]
        if all(args) is False and "Authorization" not in request.headers:
            return jsonify({
                "error": {
                    "text": "Missing one of the arguments in the data",
                    "solution": "Enter all two data keys"
                },
                "example": "requests.post('http://www.pkeorley.ml/api/v1/shortlink/create', json={'key': 'google', 'url': 'https://google.com/'}, headers={'Authorization': 'pLQNGMyCclqOOEUD'}).json()"
            })
        elif all(args) is True and "Authorization" in request.headers:
            if invites.count_documents({
                "type": "api_key",
                "key": request.headers["Authorization"]
            }) == 0:
                return jsonify({
                 "error": {
                     "text": "Invalid api key",
                     "solution": "Ask peaky to issue/replace you with a new api key"
                    }
                })
            elif invites.count_documents({
                "type": "invite",
                "key": request_json["key"]
            }) != 0:
                return jsonify({
                    "error": {
                        "text": "This key already exists",
                        "solution": "Try entering a different key name"
                    }
                })
            elif invites.find_one({
                "type": "api_key",
                "key": request.headers["Authorization"]
            })["uses"] <= 0:
                return jsonify({
                    "error": {
                        "text": "Not enough usage keys",
                        "solution": "Ask peaky to give you usage points"
                    }
                })
   
            invites.update_one({
                "type": "api_key",
                "key": request.headers["Authorization"]
            }, {"$inc": {
                "used": 1,
                "uses": -1
            }, "$push": {
                "shortlinks": request_json["key"]
            }})
            invites.insert_one({
                "type": "invite",
                "key": request_json["key"],
                "url": request_json["url"]
            })
            return jsonify({
                "result": f"http://www.pkeorley.ml/invite/{request.json['key']}"
            })

@app.route("/api/v1/shortlink/delete", methods=["GET", "POST"])
def apu_invite_delete():
    if request.method == "GET":
        args = [
            "key" in request.args,
            "api_key" in request.args
        ]
        if all(args) is False:
            return jsonify({
                "error": {
                    "text": "Missing one of the arguments in the link",
                    "solution": "Enter two arguments"
                },
                "example": "http://www.pkeorley.ml/api/v1/shortlink/delete?api_key=pLQNGMyCclqOOEUD&key=google"
            })
        elif all(args) is True:
            if invites.count_documents({
                "type": "api_key",
                "key": request.args["api_key"]
            }) == 0:
                return jsonify({
                 "error": {
                     "text": "Unknown api key",
                     "solution": "Ask peaky to issue/replace you with a new api key"
                    }
                })
            elif invites.count_documents({
                "type": "invite",
                "key": request.args["key"]
            }) == 0:
                return jsonify({
                    "error": {
                        "text": "Unknown shortlink",
                        "solution": "Enter the true shortlink which you want to delete"
                    }
                })
            elif not invites.find_one({
                "type": "api_key",
                "key": request.args["api_key"]
            })["used"] >= 0:
                return jsonify({
                    "error": {
                        "text": "Not enough points used",
                        "solution": "Create a new key"
                    }
                })
   
            shortlinks = invites.find_one({
                "type": "api_key",
                "key": request.args["api_key"]
            })["shortlinks"]
            
            index = 0
            for short in shortlinks:
                if short == request.args["key"]:
                    del shortlinks[index]
                index += 1
                
            invites.update_one({
                "type": "api_key",
                "key": request.args["api_key"]
            }, {"$inc": {
                "used": -1,
                "uses": 1
            }, "$set": {
                "shortlinks": shortlinks
            }})
            invites.delete_one({
                "type": "invite",
                "key": request.args["key"]
            })
            return jsonify({
                "result": f"Shortlink deleted"
            })
    
    
@app.route("/api/v1/shortlink/get", methods=["GET", "POST"])
def api_invite_get():
    if request.method == "GET":
        if not "api_key" in request.args:
            return jsonify({
                "error": {
                    "text": "Invalid api key",
                    "solution": "Ask peaky to issue/replace you with a new api key"
                }
            })
        
        if invites.count_documents({
            "type": "api_key",
            "key": request.args["api_key"]
        }) == 0:
            return jsonify({
                 "error": {
                     "text": "Invalid api key",
                     "solution": "Ask peaky to issue/replace you with a new api key"
                }
            })
            
        api_key = invites.find_one({
            "type": "api_key",
            "key": request.args["api_key"]
        })
        return jsonify({
            "api_key": api_key["key"],
            "stats": {
                "uses": api_key["uses"],
                "used": api_key["used"]
            },
            "shortlinks": api_key["shortlinks"]
        })


@app.route("/api/docs")
def api_docs():
    return """<h1>http://www.pkeorley.ml/api/v1</h1>
    <hr>
        <span><h3>GET <div style="color: #00ff00;">/shortlink/create</h3></div></span>
        <p>Use this method to create a new shortlink that can be clicked to.</p>
        <p>To use this method, you need an <b>api key</b>, the <b>name of the shortlink</b>, and a <b>link to which the shortlink will redirect</b></p>
        
        <p><span style="color: #ff0000;">Example:</span> http://www.pkeorley.ml/api/v1/shortlink/create?key=google&url=https://google.com/&api_key=(api_key)</p>
    
    <hr>
        <span><h3>GET <div style="color: #00ff00;">/shortlink/get</h3></div></span>
        <p>Use this method to get your IP key statistics (if you don't have it, ask the site developer for it).</p>
        <p>You need an <b>api key</b> to use this method</p>
        
        <p><span style="color: #ff0000;">Example:</span> http://www.pkeorley.ml/api/v1/shortlink/get?api_key=(api_key)</p>
        
    <hr>
        <span><h3>POST <div style="color: #00ff00;">/shortlink/create</h3></div></span>
        <p>Use this method to create a new shortlink that can be clicked to.</p>
        <p>To use this method, you need an <b>api key</b>, the <b>name of the shortlink</b>, and a <b>link to which the shortlink will redirect</b></p>
        
        <p><span style="color: #ff0000;">Example:</span> requests.post('http://www.pkeorley.ml/api/v1/shortlink/create', json={'key': 'google', 'url': 'https://google.com/'}, headers={'Authorization': 'pLQNGMyCclqOOEUD'}).json()</p>
   
   <hr>
        <span><h3>GET <div style="color: #00ff00;">/shortlink/delete</h3></div></span>
        <p>Use this method to remove shortlink from database</p>
        <p><span style="color: #ff0000;">Example:</span> http://www.pkeorley.ml/api/v1/shortlink/delete?api_key=(api_key)&key=google</p>
        
    """.replace("(api_key)", "".join(random.choice(string.ascii_letters) for x in range(16)))


if __name__ == "__main__":
    app.run(**data["run"])
