from flask import Flask
import option.server as server
from game import Setgame, Exception, User

app = Flask(__name__)

setGame = Setgame()

@app.get("/")
def main():
    return "Hello world"

@app.post("/user/register")
def register():
    data = server.get_data()
    try:
        response = setGame.check_register(data["nickname"], data["password"])
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/user/login")
def login():
    data = server.get_data()
    try:
        response = setGame.check_login(data["nickname"], data["password"])
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/room/create")
def create_room():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.create_room(player)
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/room/list")
def list_room():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.list_room(player, setGame)
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/room/enter")
def enter_room():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.enter_room(player, data["gameId"])
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/user/list")
def list_players():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.list_players(setGame)
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/field")
def get_field():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.get_field(player)
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/pick")
def pick():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.pick(player, data["cards"])
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/add")
def add():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.addCards(player)
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

@app.post("/set/scores")
def scores():
    data = server.get_data()
    try:
        player = setGame.findUserByToken(data["accessToken"])
        response = setGame.getScores(player)
        return response
    except Exception as exception:
        response = {}
        response["exception"] = exception.for_response()
        response["success"] = False
        return response

