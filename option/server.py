from flask import request


def get_data():
    data = request.get_json()
    return data

def do_response(data):
    response = {}

    for key, value in data.items():
        response[key] = value

    return response

def RegisterResponse(user):
    response = {}

    response["accessToken"] = user.token
    response["nickname"] = user.nickname

    return response

def CreateRoomResponse(gameId):
    response = {}
    response["gameId"] = gameId
    response["exception"] = None
    response["success"] = True

    return response

def ListRoomResponse(rooms):
    response = {}
    response["games"] = []

    for room in rooms:
        response["games"].append({"id": room.gameId})

    return response

def ListPlayersResponse(users):
    response = {}
    response["users"] = []

    for user in users:
        response["users"].append({"nick": user.nickname})

    return response


def EnterRoomResponse(gameId):
    response = {}
    response["gameId"] = gameId
    response["exception"] = None
    response["success"] = True

    return response

