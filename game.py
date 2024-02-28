from secrets import token_hex
from random import randint
import option.server as server

class Exception(BaseException):
    def __init__(self, text):
        self.text = text
    def for_response(self):
        return {"message": self.text}

# ----------------------------------------

class Card:
    def __init__(self, id, color, shape, fill, count):
        self.id = id
        self.color = color
        self.shape = shape
        self.fill = fill
        self.count = count
    def for_response(self):
        response = {}
        response["count"] = self.count
        response["fill"] = self.fill
        response["shape"] = self.shape
        response["color"] = self.color
        response["id"] = self.id
        return response

# ----------------------------------------

class Room:
    def __init__(self, gameId):
        self.gameId = gameId
        self.ongoing = True
        self.field = []
        self.cards = []
        self.players = []
        self.score = {}
    def findCardById(self, id):
        for card in self.field:
            if card.id == id:
                return card

        raise Exception("Card did not find")

    def createCards(self):
        id = 0
        for count in range(1, 4):
            for fill in range(1, 4):
                for shape in range(1, 4):
                    for color in range(1, 4):
                        id += 1
                        newCard = Card(id, color, shape, fill, count)
                        self.cards.append(newCard)

    def createField(self, num):
        for i in range(num):
            cord = randint(0, len(self.cards) - 1)
            self.field.append(self.cards[cord])
            self.cards.remove(self.cards[cord])

    def addPlayer(self, player):
        if player in self.players and player.idRoomActive == self.gameId:
            raise Exception("Player already in game")
        self.players.append(player)
        self.score[player.nickname] = 0
        player.idRoomActive = self.gameId

    def checkPlayers(self, player):
        if player not in self.players:
            raise Exception("Player do not in game")

# ----------------------------------------

class User:
    def __init__(self, id, nickname, password):
        self.id = id
        self.nickname = nickname
        self.password = password
        self.token = token_hex(6)
        self.idRoomActive = 0
    def __str__(self):
        return self.nickname

# ----------------------------------------
class Setgame:
    users = []
    rooms = []

    # def __init__(self, gid):
    def findUserByToken(self, token):
        for user in self.users:
            if user.token == token:
                return user

        raise Exception("Player did not find")

    def findRoomById(self, gameId):
        for room in self.rooms:
            if room.gameId == gameId:
                return room

        raise Exception("Room did not find")

    def check_register(self, nickname, password):
        if nickname == "":
            raise Exception("Prohibited nickname")

        for user in self.users:
            if user.nickname == str(nickname):
                raise Exception("Nickname already exist")

        newUser = User(len(self.users) + 1, nickname, password)
        self.users.append(newUser)

        return server.RegisterResponse(newUser)

    def check_login(self, nickname, password):
        for user in self.users:
            if user.nickname == str(nickname):
                if user.password == str(password):
                    user.token = token_hex(6)
                    return server.RegisterResponse(user)
                else:
                    raise Exception("Password uncorrect")

        raise Exception("Nickname did not find")

    def create_room(self, player):
        newRoom = Room(len(self.rooms) + 1)
        newRoom.addPlayer(player)
        newRoom.createCards()
        newRoom.createField(12)
        newRoom.score[player.nickname] = 0
        self.rooms.append(newRoom)


        return server.CreateRoomResponse(newRoom.gameId)

    def list_room(self, player, setGame):
        return server.ListRoomResponse(setGame.rooms)

    def list_players(self, setGame):
        return server.ListPlayersResponse(setGame.users)

    def enter_room(self, player, gameId):
        room = self.findRoomById(gameId)
        room.addPlayer(player)
        return server.EnterRoomResponse(gameId)

    def get_field(self, player):
        room = self.findRoomById(player.idRoomActive)
        room.checkPlayers(player)
        response = {}
        response["cards"] = []
        for card in room.field:
            response["cards"].append(card.for_response())
        response["status"] = room.ongoing
        response["score"] = room.score[player.nickname]
        return response

    def findSet(self, room):
        for i in range(len(room.field)):
            for j in range(len(room.field)):
                if i == j:
                    continue
                firstCard = room.field[i]
                secondCard = room.field[j]

                if firstCard.fill == secondCard.fill:
                    neededFill = firstCard.fill
                else:
                    neededFill = 6 - firstCard.fill - secondCard.fill

                if firstCard.color == secondCard.color:
                    neededColor = firstCard.color
                else:
                    neededColor = 6 - firstCard.color - secondCard.color

                if firstCard.shape == secondCard.shape:
                    neededShape = firstCard.shape
                else:
                    neededShape = 6 - firstCard.shape - secondCard.shape

                if firstCard.count == secondCard.count:
                    neededCount = firstCard.count
                else:
                    neededCount = 6 - firstCard.count - secondCard.count

                for k in range(len(room.field)):
                    if i != k and j != k:
                        if room.field[k].fill == neededFill and room.field[k].color == neededColor and room.field[k].shape == neededShape and room.field[k].count == neededCount:
                            print(firstCard.id, secondCard.id, room.field[k].id)

                            return True
        return False

    def pick(self, player, cards):
        if len(cards) != 3:
            raise Exception("Wrong number of cards")

        room = self.findRoomById(player.idRoomActive)
        room.checkPlayers(player)

        firstCard = room.findCardById(cards[0])
        secondCard = room.findCardById(cards[1])
        thirdCard = room.findCardById(cards[2])
        isSet = False

        if (firstCard.fill == secondCard.fill == thirdCard.fill) or (6 - firstCard.fill - secondCard.fill - thirdCard.fill == 0):
            if (firstCard.color == secondCard.color == thirdCard.color) or (6 - firstCard.color - secondCard.color - thirdCard.color == 0):
                if (firstCard.count == secondCard.count == thirdCard.count) or (6 - firstCard.count - secondCard.count - thirdCard.count == 0):
                    if (firstCard.shape == secondCard.shape == thirdCard.shape) or (6 - firstCard.shape - secondCard.shape - thirdCard.shape == 0):
                        isSet = True

        response = {}
        if isSet:
            room.score[player.nickname] = room.score[player.nickname] + 1
            room.field.remove(firstCard)
            room.field.remove(secondCard)
            room.field.remove(thirdCard)
            if not(self.findSet(room)) and len(room.cards) == 0:
                room.ongoing = False

            if len(room.field) == 9:
                if len(room.cards) < 3:
                    room.createField(len(room.cards))
                else:
                    room.createField(3)




        response["score"] = room.score[player.nickname]
        response["isSet"] = isSet

        return response

    def addCards(self, player):
        room = self.findRoomById(player.idRoomActive)
        room.checkPlayers(player)

        room.createField(3)

        response = {}
        response["success"] = True
        response["exception"] = "null"

        return response

    def getScores(self, player):
        room = self.findRoomById(player.idRoomActive)
        room.checkPlayers(player)

        response = {}

        response["success"] = True
        response["exception"] = "null"

        response["users"] = []
        for name, score in room.score.items():
            response["users"].append({"name": name, "score": score})


        return response
