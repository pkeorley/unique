import asyncio

from quart import Quart
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from config import data


app = Quart(__name__)
app.config["SECRET_KEY"] = data["secret_key"]
app = MongoClient(data["mongo_client"])
mongo.get_io_loop = asyncio.get_running_loop


@app.route("/", methods=["GET"])
async def index():
    return "<h1>Hello, world!</h1>"


@app.route("/config")
async def secretkey():
    return data


if __name__ == "__main__":
    run = data["run"]
    app.run(
        debug=run["debug"],
        threaded=run["threaded"]
    )
